import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode

from pprint import pprint


class Vk:
    session = None
    vk = None
    # user_id => name
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
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        # lazy
                        event._process_message = self.process_message

                        callback(event)
                break
            except Exception as e:
                print("vk listen() exception:")
                print(e)
                continue

    def process_message(self, event):
        text = ""
        if event.attachments:
            full_message = self.load_full_message(event.message_id)
            print("--------")
            pprint(full_message)
            print("--------")
            text = self.recursive_process_message(full_message)
        else:
            author_id = None
            if hasattr(event, "user_id"):
                author_id = event.user_id
            if hasattr(event, "group_id"):
                author_id = event.group_id

            text = self.get_id_name(author_id) + ": " + event.message

        return text

    def load_full_message(self, message_id):
        return self.vk.messages.getById(message_ids=message_id)["items"][0]

    def recursive_process_message(self, message):
        text = self.get_id_name(abs(message["from_id"])) + ": " + message["text"]

        for attach in message["attachments"]:
            if "photo" in attach.keys():
                # sort them by size
                # doc: https://dev.vk.com/ru/reference/objects/photo-sizes
                photos = sorted(
                    attach["photo"]["sizes"], key=lambda x: x["width"] * x["height"]
                )
                text += "\nPhoto: " + photos[-1]["url"]
            if "sticker" in attach.keys():
                text += "\nSticker: " + attach["sticker"]["images"][-1]["url"]
            if "audio_message" in attach.keys():
                # TODO: ogg or mp3?
                text += "\nVoice: " + attach["audio_message"]["link_ogg"]
            if "doc" in attach.keys():
                text += "\nDocument: " + attach["doc"]["url"]
            if "link" in attach.keys():
                text += "\nLink: " + attach["link"]["url"]
            if "video" in attach.keys():
                video = attach["video"]
                url = "vk.com/video{0}_{1}".format(video["owner_id"], video["id"])
                text += "\nVideo: " + url
            if "wall" in attach.keys():
                wall = attach["wall"]
                url = "<code>vk.com/wall{0}_{1}</code>".format(wall["owner_id"], wall["id"])
                text += "\nWall: {0}\n".format(url)
                text += self.recursive_process_message(wall)
            if "wall_reply" in attach.keys():
                wall_reply = attach["wall_reply"]
                url = "<code>vk.com/wall{0}_{1}?reply={2}</code>".format(wall_reply["owner_id"], wall_reply["post_id"], wall_reply["id"])
                text += "\nWall reply: {0}\n".format(url)
                text += self.recursive_process_message(wall_reply)

        if "reply_message" in message.keys():
            reply = message["reply_message"]
            text += "\n---\nReplied to: "
            text += self.recursive_process_message(reply)
        if "fwd_messages" in message.keys():
            fwds = message["fwd_messages"]
            for fwd in fwds:
                text += "\n---\nForwarded: "
                text += self.recursive_process_message(fwd)

        return text

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
