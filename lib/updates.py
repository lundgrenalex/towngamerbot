from lib import telegram as tg
from config import telegram_key
from lib import callbacks, messages
import logging


def process(updates: list):

    for message in updates:

        if 'message' in message:
            logging.info(message)
            messages.process(message)
            continue

        if 'callback_query' in message:
            callbacks.process(message)
            continue

        else:
            logging.info("Non-processing msg:\n", message)
