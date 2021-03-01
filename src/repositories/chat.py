from src.services.telegram import TelegramBotApi
from src.settings.config import telegram_key as token


class Chat:

    def __init__(self, chat_id:int = ""):
        self.chat_id = chat_id

    def message(self, message):
        bot_api = TelegramBotApi(token)
        return bot_api.send_message(self.chat_id, message=message)
