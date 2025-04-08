import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode
from pprint import pprint

from downloading_files import download_video
from parsed_message import ParsedMessage

MAX_VIDEO_DURATION_TO_REUPLOAD = 6 * 30


class Vk:
    session = None
    vk = None
    names = {}

    def __init__(self, token):
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()

    def listen(self, callback):
        print("Listening")
        pprint(self.names)

        longpoll = VkLongPoll(self.session, mode=VkLongpollMode.GET_ATTACHMENTS)

        # sometimes vk listen may fail with timeout, so try until successful
        while True:
            try:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        # lazy
                        event._process_message = self.process_message

                        callback(event)
                break
            except Exception as e:
                print("vk listen() exception:")
                print(e)
                continue

    def process_message(self, event):
        res = ParsedMessage()

        if event.attachments:
            full_message = self.load_full_message(event.message_id)
            print("--------")
            pprint(full_message)
            print("--------")
            res += self.recursive_process_message(full_message)
        else:
            author_id = None
            if hasattr(event, "user_id"):
                author_id = event.user_id
            if hasattr(event, "group_id"):
                author_id = event.group_id

            res.text += self.get_id_name(author_id) + ": " + event.message

        return res

    def load_full_message(self, message_id):
        return self.vk.messages.getById(message_ids=message_id)["items"][0]

    def recursive_process_message(self, message):
        res = ParsedMessage()
        res.text = self.get_id_name(abs(message["from_id"])) + ": " + message["text"]

        for attach in message["attachments"]:
            if "photo" in attach.keys():
                # sort them by size
                # doc: https://dev.vk.com/ru/reference/objects/photo-sizes
                photos = sorted(
                    attach["photo"]["sizes"], key=lambda x: x["width"] * x["height"]
                )
                res.add_preview(format_hyperlink("image", photos[-1]["url"]))
            if "sticker" in attach.keys():
                sticker_url = attach["sticker"]["images"][-1]["url"]
                res.text += format_hyperlink("sticker", sticker_url)
            if "audio_message" in attach.keys():
                # TODO: ogg or mp3?
                voice_url = attach["audio_message"]["link_ogg"]
                res.add_preview(format_hyperlink("voice message", voice_url))
            if "doc" in attach.keys():
                res.add_preview(format_hyperlink("document", attach["doc"]["url"]))
            if "link" in attach.keys():
                res.text += "\nLink: " + attach["link"]["url"]
            if "audio" in attach.keys():
                # audios not really supported, here just showing artist and
                # title of the track
                audio = attach["audio"]
                res.text += "\nAudio (reuploading not supported): {0} - {1}".format(
                    audio["artist"], audio["title"]
                )
            if "video" in attach.keys():
                video = attach["video"]
                if video["duration"] > MAX_VIDEO_DURATION_TO_REUPLOAD:
                    url = "vk.com/video{0}_{1}".format(video["owner_id"], video["id"])
                    res.text += "\nVideo: " + url
                else:
                    res.video_downloaded_file = download_video(video["player"])
                    res.text += "\n*video (see uploaded file)*"
            if "wall" in attach.keys():
                wall = attach["wall"]
                url = "<code>vk.com/wall{0}_{1}</code>".format(
                    wall["owner_id"], wall["id"]
                )
                res.text += "\nWall: {0}\n".format(url)
                res += self.recursive_process_message(wall)
                if "copy_history" in wall.keys():
                    for repost in wall["copy_history"]:
                        res.text += "\nWall repost:\n"
                        res += self.recursive_process_message(repost)
            if "wall_reply" in attach.keys():
                # wall reply is a comment on wall post
                wall_reply = attach["wall_reply"]
                url = "<code>vk.com/wall{0}_{1}?reply={2}</code>".format(
                    wall_reply["owner_id"], wall_reply["post_id"], wall_reply["id"]
                )
                res.text += "\nWall reply: {0}\n".format(url)
                res += self.recursive_process_message(wall_reply)
            if "graffiti" in attach.keys():
                graffiti = attach["graffiti"]
                res.add_preview(format_hyperlink("graffiti", graffiti["url"]))

        if "reply_message" in message.keys():
            reply = message["reply_message"]
            res.text += "\n---\nReplied to: "
            res += self.recursive_process_message(reply)
        if "fwd_messages" in message.keys():
            fwds = message["fwd_messages"]
            for fwd in fwds:
                res.text += "\n---\nForwarded: "
                res += self.recursive_process_message(fwd)

        return res

    def get_id_name(self, id):
        if id in self.names:
            return self.names[id]
        else:
            return "id_" + str(id)

    def update_parse_names(self, peer_id):
        response = self.vk.messages.getConversationMembers(peer_id=peer_id)
        res = {}
        for x in response["profiles"]:
            id = x["id"]
            name = x["first_name"] + " " + x["last_name"]
            self.names[id] = name
        if "groups" in response.keys():
            for x in response["groups"]:
                id = x["id"]
                name = x["name"]
                self.names[id] = name

        return res


def format_hyperlink(text, url):
    return "\n<a href='{0}'>*{1}*</a>".format(url, text)
