import logging
from . import commands
from .game import cities
from .game import CityGame
from lib import helpers
from lib.messages.chat import Chat


def is_command(message: dict) -> bool:
    if 'entities' not in message['message']:
        return False
    for entity in message['message']['entities']:
        if entity['type'] == 'bot_command':
            return True
    return False

def process(message: dict):
    if is_command(message):
        commands.process(message)
        return
    process_message(message)

def send_bot_answer(message: dict):

    chat_id = message['message']['chat']['id']

    g = CityGame(message=message)
    chat = Chat(chat_id=message['message']['chat']['id'])

    bot_answer = g.get_new_answer()
    if not bot_answer:

        # Get score for username
        chat.message(
            helpers.render_template(
                'winner',
                message['message']['chat']['username'],
                g.get_score()))

        # Cancel game
        g.cancel()

        return False

    result = chat.message(bot_answer)

    # write bot answer
    result = g.save_bot_answer(result)
    logging.info(result)

    return True


def process_message(message: dict):

    # init Game
    g = CityGame(message=message)

    chat = Chat(chat_id=message['message']['chat']['id'])

    # get current city
    city = message['message']['text']

    # Checing bot
    if message['message']['from']['is_bot']:
        return False

    # dirty words
    if helpers.check_obscenity(city):
        chat.message('Не ругайся матом тупая ты скотина!')
        return False

    # game exists
    if not g.exists():
        chat.message('Вы еще не начали, нажмите /start чтобы поиграть в города!')
        return False

    # get last answer
    last_answer = g.get_last_answer()

    # check prevoius answers
    if g.is_answered_city():
        chat.message(f'Город {city} уже использовали в ответах!')
        return False

    # check last symbol from last answer
    if not helpers.is_word_in_chain(last_answer['message'], message['message']['text']):
        err_msg = f"Ваш город {message['message']['text']} не начинается с последнего символа предыдущего города {last_answer['message']} из ответов"
        chat.message(err_msg)
        return False

    # city exists
    if not cities.city_exists(city):
        chat.message(f'Города {city} не существует!')
        return False

    # save user answer
    g.save_user_answer()

    # send bot answer
    send_bot_answer(message)
