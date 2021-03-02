import logging

from src.use_cases.telegram.bot import TelegramBot
from src.use_cases.telegram.messages import TelegramMessage
from src.use_cases.telegram.commands import TelegramCommand


logging.basicConfig(
    format='%(asctime)-15s %(levelname)-8s %(name)-1s: %(message)s',
    level=logging.DEBUG)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


if __name__ == '__main__':
    bot = TelegramBot()
    bot.register_observer('message', TelegramMessage())
    bot.register_observer('command', TelegramCommand())
    bot.run()
