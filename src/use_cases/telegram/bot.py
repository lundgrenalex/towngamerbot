import time
from requests.exceptions import ReadTimeout, ConnectionError

from src.libs.telegram import TelegramMessageObservable
from src.drivers.telegram import TelegramBotApi
from src.adapters.telegram import TelegramMessageAdapter
from src.settings.config import telegram_key as token


class TelegramBot(TelegramMessageObservable):

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
