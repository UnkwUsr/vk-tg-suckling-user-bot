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

        text = event._author_name + ": " + event.text

        if event.attachments:
            text += "\n---\nAttachments: \n" + json.dumps(event.attachments)

        self.tg.send_message(chat_id=self.out_tg_chat_id, text=text)
