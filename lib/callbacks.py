import logging
from lib.storage import cities
from lib.storage import game
from lib import telegram
from config import telegram_key


def process(message: dict):
    logging.info('Callback: ', message)
    return
