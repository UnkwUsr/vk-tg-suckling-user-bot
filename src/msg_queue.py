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

        # sometimes telegram fails, so try until successful
        while True:
            try:
                for x in smart_split(msg.text):
                    self.tg.send_message(
                        chat_id=self.out_tg_chat_id, text=x, parse_mode="html"
                    )
                if msg.video_downloaded_file:
                    video = msg.video_downloaded_file
                    print("Video file:", video)
                    self.tg.send_video(
                        chat_id=self.out_tg_chat_id,
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
