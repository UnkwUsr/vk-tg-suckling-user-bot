import telebot

from vk import Vk
from pprint import pprint
from msg_queue import Queue
import config


def vk_on_message(event):
    pprint(vars(event))

    event._get_id_name = lambda x: vk_names[x] if x in vk_names else "id_" + str(x)

    for q in qs:
        q.on_in_message(event)


def init_bridges():
    global qs
    global vk_names
    for x in config.bridges:
        q = Queue(in_vk_peer_id=x["vk_peer_id"], out_tg_chat_id=x["tg_chat_id"], tg=tg)
        qs.append(q)

        vk_names.update(vk_parse_names(vk, x["vk_peer_id"]))


def vk_parse_names(vk, peer_id):
    response = vk.vk.messages.getConversationMembers(peer_id=peer_id)
    res = {}
    for x in response["profiles"]:
        id = x["id"]
        name = x["first_name"] + " " + x["last_name"]
        vk_names[id] = name
    if "groups" in response.keys():
        for x in response["groups"]:
            id = x["id"]
            name = x["name"]
            vk_names[id] = name

    return res


vk = Vk(config.VK_TOKEN)
tg = telebot.TeleBot(config.TG_TOKEN)


# queues
qs = []
# user_id => name
vk_names = {}

init_bridges()
pprint(vk_names)

vk.listen(vk_on_message)
