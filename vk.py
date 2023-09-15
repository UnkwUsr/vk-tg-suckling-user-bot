import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Vk:
    session = None
    vk = None

    def __init__(self, token):
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()

    def listen(self, callback):
        print("Listening")

        longpoll = VkLongPoll(self.session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                callback(event)
