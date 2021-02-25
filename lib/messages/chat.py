from lib.messages import telegram
from config import telegram_key


class Chat:

    def __init__(self, chat_id:int = ""):
        self.chat_id = chat_id

    def message(self, message):
        return telegram.send_message(
            self.chat_id,
            message=message,
            bot_token=telegram_key)
