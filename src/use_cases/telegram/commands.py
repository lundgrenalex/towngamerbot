import logging

from src.libs import helpers
from src.repositories.city import CityRepositoRy
from src.repositories.game import GameRepository
from src.domain.answer import Answer
from src.repositories.answer import AnswerRepository
from src.libs.telegram import TelegramMessageObserver


class TelegramCommand(TelegramMessageObserver):

    def add(self, message: str) -> None:
        self.message = message
        self.text = message['message']['text']
        self.answer_repository = AnswerRepository()
        self.game = GameRepository(message=self.message)
        self.process_command(self.message['meta']['command'])

    def process_command(self, name: str):
        try:
            return getattr(self, name)()
        except AttributeError:
            logging.error(f'Command /{name} not found!')

    def stop(self) -> None:

        if not self.game.exists():
            self.game.chat.message('Вы еще не начали, нажмите /start чтобы начать играть в города!')
            return

        score = int(self.game.get_score() * 0.75)
        self.game.chat.message(helpers.render_template(
            'stopped', self.message['message']['chat']['username'], score))

        self.game.cancel()

    def start(self):

        if self.game.exists():
            self.game.chat.message('Вы еще не закончили последнюю игру, нажмите /stop или говорите город!')
            return

        city = CityRepositoRy().random()

        message_status = self.game.chat.message(city)
        logging.info(message_status)

        result = self.answer_repository.save(Answer(
            chat_id=message_status['result']['chat']['id'],
            user_id=message_status['result']['from']['id'],
            message=message_status['result']['text']))
        logging.info(result)

        return

    def hint(self):
        return self.game.chat.message(self.game.get_hint())
