import json


class Queue:
    in_vk_peer_id = None
    out_tg_chat_id = None
    tg = None

    def __init__(self, in_vk_peer_id, out_tg_chat_id, tg):
        self.in_vk_peer_id = in_vk_peer_id
        self.out_tg_chat_id = out_tg_chat_id
        self.tg = tg

    def on_in_message(self, event):
        if event.peer_id != self.in_vk_peer_id:
            return

        author_id = None
        if hasattr(event, "user_id"):
            author_id = event.user_id
        if hasattr(event, "group_id"):
            author_id = event.group_id

        text = event._get_id_name(author_id) + ": " + event.message

        if event.attachments:
            attachments = event._load_attachments()["items"]
            for item in attachments:
                if "reply_message" in item.keys():
                    # TODO: probably also take attachments from there,
                    # recursive
                    reply = item["reply_message"]
                    text += (
                        "\n---\nReplied to: "
                        + event._get_id_name(abs(reply["from_id"]))
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
                            + event._get_id_name(abs(fwd["from_id"]))
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

        # sometimes telegram fails, so try until succesfull
        while True:
            try:
                self.tg.send_message(chat_id=self.out_tg_chat_id, text=text)
                break
            except Exception as e:
                print("tg send_message exception:")
                print(e)
                continue
