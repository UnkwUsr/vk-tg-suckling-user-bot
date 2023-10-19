import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode

import json
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

        # sometimes vk listen may fail with timeout, so try until succesfull
        while True:
            try:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        # lazy
                        event._load_attachments = lambda: self.vk.messages.getById(
                            message_ids=event.message_id
                        )
                        event._process_message = self.process_message

                        callback(event)
                break
            except Exception as e:
                print("vk listen() exception:")
                print(e)
                continue

    def process_message(self, event):
        author_id = None
        if hasattr(event, "user_id"):
            author_id = event.user_id
        if hasattr(event, "group_id"):
            author_id = event.group_id

        text = self.get_id_name(author_id) + ": " + event.message

        if event.attachments:
            attachments = event._load_attachments()["items"]
            for item in attachments:
                print("Attachment: ", end="")
                pprint(item)
                if "reply_message" in item.keys():
                    # TODO: probably also take attachments from there,
                    # recursive
                    reply = item["reply_message"]
                    text += (
                        "\n---\nReplied to: "
                        + self.get_id_name(abs(reply["from_id"]))
                        + ": "
                        + reply["text"]
                    )
                if "fwd_messages" in item.keys():
                    # TODO: probably also take attachments from there,
                    # recursive
                    fwds = item["fwd_messages"]
                    for fwd in fwds:
                        text += (
                            "\n---\nForwarded: "
                            + self.get_id_name(abs(fwd["from_id"]))
                            + ": "
                            + fwd["text"]
                        )
                        # stub, we do not support deep forwarded messages. On
                        # the other hand, vk does the same on the site. But api
                        # in real returns all forwards chain
                        if "fwd_messages" in fwd.keys():
                            text += "*reforwarded messages*"

                # yes, yet another attribute with name "attachments"
                for itach in item["attachments"]:
                    if "photo" in itach.keys():
                        # TOOD: probably should take proper size. Some of them
                        # can be cropped, this is bad
                        # https://dev.vk.com/ru/reference/objects/photo-sizes
                        text += "\nPhoto: " + itach["photo"]["sizes"][-1]["url"]
                    if "audio_message" in itach.keys():
                        # TODO: ogg or mp3?
                        text += "\nVoice: " + itach["audio_message"]["link_ogg"]

            text += "\n---\nRaw attachments: \n" + json.dumps(event.attachments)

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
