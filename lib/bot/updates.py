from . import callbacks
from . import messages
import logging


def process(updates: list):

    for message in updates:

        if 'message' in message:
            messages.process(message)
            continue

        if 'callback_query' in message:
            callbacks.process(message)
            continue

        else:
            logging.info("Non-processing msg:\n", message)
