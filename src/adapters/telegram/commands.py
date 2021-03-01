import re
import json
import logging
from src.libs import helpers
from src.repositories.city import City
from src.repositories.game import CityGame


class TelegramCommand:

    def __init__(message: dict):
        self.message = message
        self.game = CityGame(message=self.message)
        self.process()

    def process(self) -> None:
        self.start()
        self.stop()
        self.hint()

    def stop(self) -> None:

        if not re.search(r'\/stop', self.message['message']['text']):
            return

        if not self.game.exists():
            self.game.chat.message('Вы еще не начали, нажмите /start чтобы начать играть в города!')
            return

        # Get score for username and send message
        score = int(self.game.get_score() * 0.75)
        self.game.chat.message(helpers.render_template(
            'stopped', self.message['message']['chat']['username'], score))

        # Cancel game
        self.game.cancel()


    def start(self):

        if not re.search(r'\/start', self.message['message']['text']):
            return

        if self.game.exists():
            self.game.chat.message('Вы еще не закончили последнюю игру, нажмите /stop или говорите город!')
            return

        # Get random city
        city = cities.get_random()

        # send_message
        result = self.game.chat.message(city)
        logging.info(result)

        # write bot answer
        result = self.game.save_bot_answer(result)
        logging.info(result)

        return

    def hint(self):

        if not re.search(r'\/hint', self.message['message']['text']):
            return

        return self.game.chat.message(self.game.get_hint())
