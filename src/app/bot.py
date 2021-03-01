import requests
import logging
import time

from src.use_cases.telegram.updates import TelegramUpdates

logging.basicConfig(
    format='%(asctime)-15s %(levelname)-8s %(name)-1s: %(message)s',
    level=logging.DEBUG)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


if __name__ == '__main__':
    TelegramUpdates().get()
