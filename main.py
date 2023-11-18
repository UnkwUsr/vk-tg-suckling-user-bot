import telebot

from vk import Vk
from pprint import pprint
from msg_queue import Queue
import config


def vk_on_message(event):
    pprint(vars(event))

    for q in queues:
        q.on_in_message(event)


def init_bridges():
    global queues
    for x in config.bridges:
        q = Queue(in_vk_peer_id=x["vk_peer_id"], out_tg_chat_id=x["tg_chat_id"], tg=tg)
        queues.append(q)

        vk.update_parse_names(x["vk_peer_id"])


vk = Vk(config.VK_TOKEN)
tg = telebot.TeleBot(config.TG_TOKEN)


# queues
queues = []

init_bridges()

vk.listen(vk_on_message)
