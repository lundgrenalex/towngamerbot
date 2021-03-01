import time


class Answer(object):

    def __init__(self, chat_id: int, user_id: int, message: str) -> None:
        self.date = time.time()
        self.chat_id = chat_id
        self.user_id = user_id
        self.message = message
