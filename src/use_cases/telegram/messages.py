import logging

from src.libs import helpers
from src.domain.answer import Answer
from src.repositories.answer import AnswerRepository
from src.repositories.city import City
from src.repositories.game import CityGame
from src.libs.observer import Observer


class TelegramMessage(Observer):

    def add(self, message: dict):
        self.message = message
        self.answer_repository = AnswerRepository()
        self.game = CityGame(message=self.message)
        self.process_user_message()

    def send_bot_answer(self) -> None:
        bot_answer = self.game.get_new_answer()
        if not bot_answer:
            self.game.chat.message(
                helpers.render_template(
                    'winner',
                    self.message['message']['chat']['username'],
                    self.game.get_score()))
            self.game.cancel()
            return

        message_status = self.game.chat.message(bot_answer)
        self.answer_repository.save(Answer(
            chat_id=message_status['result']['chat']['id'],
            user_id=message_status['result']['from']['id'],
            message=message_status['result']['text']))
        return

    def process_user_message(self) -> None:

        city = self.message['message']['text']

        if self.message['message']['from']['is_bot']:
            return

        if helpers.check_obscenity(city):
            self.game.chat.message('Не ругайся матом тупая ты скотина!')
            return

        if not self.game.exists():
            self.game.chat.message('Вы еще не начали, нажмите /start чтобы поиграть в города!')
            return

        if self.game.is_answered_city():
            self.game.chat.message(f'Город {city} уже использовали в ответах!')
            return

        last_answer = self.game.get_last_answer()
        if not helpers.is_word_in_chain(last_answer['message'], city):
            self.game.chat.message(
                helpers.render_template(
                    'wrong_city',
                    self.message['message']['text'],
                    last_answer['message']))
            return

        if not City().exists(city):
            self.game.chat.message(f'Города {city} не существует!')
            return

        self.answer_repository.save(Answer(
            chat_id=self.message['message']['chat']['id'],
            user_id=self.message['message']['from']['id'],
            message=self.message['message']['text']))
        self.send_bot_answer()
