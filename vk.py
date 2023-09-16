import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode


class Vk:
    session = None
    vk = None

    def __init__(self, token):
        self.session = vk_api.VkApi(token=token)
        self.vk = self.session.get_api()

    def listen(self, callback):
        print("Listening")

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

                        callback(event)
                break
            except Exception as e:
                print("vk listen() exception:")
                print(e)
                continue
