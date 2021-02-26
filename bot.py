import requests
import time
from lib.messages.telegram import TelegramBotApi
from lib.bot import updates
import logging

from config import telegram_key as token

updates_offset = 0

logging.basicConfig(
    format='%(asctime)-15s %(levelname)-8s %(name)-1s: %(message)s',
    level=logging.DEBUG,
)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Init telegram bot connection
bot_api = TelegramBotApi(token)

while True:

    try:
        params = {} if updates_offset == 0 else {'offset': updates_offset}
        _updates = bot_api.get_updates(params)['result']
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
        updates_offset = int(_updates[-1:][0]['update_id']) + 1
    except IndexError:
        time.sleep(0.5)
        continue

    if not _updates:
        logging.error('No messages!')
        continue

    updates.process(_updates)
