import time
import logging
import requests

from src.drivers.telegram import TelegramBotApi
from src.use_cases.telegram.messages import TelegramMessage
from src.settings.config import telegram_key as token
from . import callbacks
from . import messages

class TelegramUpdates:

    def __init__(self):
        self.offset = 0
        self.bot_api = TelegramBotApi(token)

    def get(self):

        while True:
            try:
                params = {} if self.offset == 0 else {'offset': self.offset}
                _updates = self.bot_api.get_updates(params)['result']
            except KeyError:
                logging.error('Without updates!')
                time.sleep(0.5)
                continue
            except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError):
                logging.error('api.telegram.org read timed out!')
                time.sleep(0.5)
                continue

            _updates = sorted(_updates, key = lambda i: i['update_id'])

            try:
                self.offset = int(_updates[-1:][0]['update_id']) + 1
            except IndexError:
                time.sleep(0.5)
                continue

            if not _updates:
                logging.error('No messages!')
                continue

            for message in _updates:

                if 'message' in message:
                    TelegramMessage(message).process()
                    continue

                if 'callback_query' in message:
                    callbacks.process(message)
                    continue

                else:
                    logging.info("Non-processing msg:\n", message)
