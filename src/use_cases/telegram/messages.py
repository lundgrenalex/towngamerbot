import logging

from src.use_cases.telegram.commands import TelegramCommand
from src.libs import helpers
from src.domain.answer import Answer
from src.repositories.answer import AnswerRepository
from src.repositories.city import City
from src.repositories.game import CityGame


class TelegramMessage:

    def __init__(self, message: dict):
        self.message = message
        self.game = CityGame(message=self.message)
        self.answer_repository = AnswerRepository()

    def is_command(self) -> bool:
        if 'entities' not in self.message['message']:
            return False
        for entity in self.message['message']['entities']:
            if entity['type'] == 'bot_command':
                return True
        return False

    def process(self):
        if self.is_command():
            return TelegramCommand(self.message).process()
        self.process_message()

    def send_bot_answer(self):

        bot_answer = self.game.get_new_answer()
        if not bot_answer:

            # Get score for username
            self.game.chat.message(
                helpers.render_template(
                    'winner',
                    self.message['message']['chat']['username'],
                    self.game.get_score()))

            # Cancel game
            self.game.cancel()

            return False

        message_status = self.game.chat.message(bot_answer)

        # write bot answer
        result = self.answer_repository.save(Answer(
            chat_id=message_status['result']['chat']['id'],
            user_id=message_status['result']['from']['id'],
            message=message_status['result']['text']))
        logging.info(result)

        return True

    def process_message(self):

        # get current city
        city = self.message['message']['text']

        # Checing bot
        if self.message['message']['from']['is_bot']:
            return False

        # dirty words
        if helpers.check_obscenity(city):
            self.game.chat.message('Не ругайся матом тупая ты скотина!')
            return False

        # game exists
        if not self.game.exists():
            self.game.chat.message('Вы еще не начали, нажмите /start чтобы поиграть в города!')
            return False

        # get last answer
        last_answer = self.game.get_last_answer()

        # check prevoius answers
        if self.game.is_answered_city():
            self.game.chat.message(f'Город {city} уже использовали в ответах!')
            return False

        # check last symbol from last answer
        if not helpers.is_word_in_chain(last_answer['message'], city):
            err_msg = f"""
            Ваш город {self.message['message']['text']} не начинается
            с последнего символа предыдущего города
            {last_answer['message']} из ответов
            """
            self.game.chat.message(err_msg)
            return False

        # city exists
        if not City().exists(city):
            self.game.chat.message(f'Города {city} не существует!')
            return False

        # save user answer
        self.answer_repository.save(Answer(
            chat_id=self.message['message']['chat']['id'],
            user_id=self.message['message']['from']['id'],
            message=self.message['message']['text'],
        ))

        # send bot answer
        self.send_bot_answer()
