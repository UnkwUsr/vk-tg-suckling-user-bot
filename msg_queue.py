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
                    reply = item["reply_message"]
                    text += (
                        "\n---\nReplied to: "
                        + event._get_id_name(abs(reply["from_id"]))
                        + ": "
                        + reply["text"]
                    )

            text += "\n---\nRaw attachments: \n" + json.dumps(event.attachments)

        self.tg.send_message(chat_id=self.out_tg_chat_id, text=text)
