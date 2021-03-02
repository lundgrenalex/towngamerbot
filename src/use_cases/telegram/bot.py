import time
import logging
from requests.exceptions import ReadTimeout, ConnectionError

from src.libs.observer import Observable
from src.drivers.telegram import TelegramBotApi
from src.use_cases.telegram.messages import TelegramMessage
from src.adapters.telegram import TelegramMessageAdapter
from src.settings.config import telegram_key as token
from . import callbacks


class TelegramBot(Observable):

    def __init__(self):
        self.offset = 0
        self.sleep_time = 0.5
        self.bot_api = TelegramBotApi(token)

    def process(self, message: dict) -> None:
        self.notify_observers(message)

    def get_updates(self):
        try:
            params = {} if self.offset == 0 else {'offset': self.offset}
            updates = self.bot_api.get_updates(params)['result']
            updates = sorted(updates, key=lambda i: i['update_id'])
            self.offset = int(updates[-1:][0]['update_id']) + 1
        except (KeyError, ReadTimeout, ConnectionError, IndexError):
            updates = []
        return updates

    def run(self) -> None:
        while True:
            for message in self.get_updates():
                self.process(TelegramMessageAdapter(message).add_meta())
            time.sleep(self.sleep_time)
