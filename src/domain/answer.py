class Answer(object):

    def __init__(self, chat_id: int, user_id: int, date: int, message: str) -> None:
        self.date = date
        self.chat_id = chat_id
        self.user_id = user_id
        self.message = message
