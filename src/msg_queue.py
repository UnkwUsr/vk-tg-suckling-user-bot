import time
from telebot.util import smart_split
from telebot.types import InputFile

from downloading_files import cleanup_temp_dir_video


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

        msg = event._process_message(event)

        # hack: always append first preview to text message
        if len(msg.previews) > 0:
            msg.text += msg.previews.pop(0)

        # sometimes telegram fails, so try until successful
        while True:
            try:
                sent_txt_tg_msg = None
                # send message with text (can be splitted if too long)
                for x in smart_split(msg.text):
                    sent_txt_tg_msg = self.tg.send_message(
                        chat_id=self.out_tg_chat_id, text=x, parse_mode="html"
                    )
                # send messages with preview images
                for p in msg.previews:
                    self.tg.send_message(
                        chat_id=self.out_tg_chat_id,
                        reply_to_message_id=sent_txt_tg_msg.message_id,
                        text=p,
                        parse_mode="html",
                    )
                # send video file
                if msg.video_downloaded_file:
                    video = msg.video_downloaded_file
                    print("Video file:", video)
                    self.tg.send_video(
                        chat_id=self.out_tg_chat_id,
                        reply_to_message_id=sent_txt_tg_msg.message_id,
                        video=InputFile(video),
                    )
                    cleanup_temp_dir_video(video)
                break
            except Exception as e:
                print("tg send_message exception:")
                print(e)
                time.sleep(5)
                continue

        # log separator between events
        print()
