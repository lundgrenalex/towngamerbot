import logging
from . import commands
from lib.game import cities
from lib.game import CityGame
from lib import helpers


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

    game = CityGame(message=message)

    bot_answer = game.get_new_answer()
    if not bot_answer:

        # Get score for username
        game.chat.message(
            helpers.render_template(
                'winner',
                message['message']['chat']['username'],
                game.get_score()))

        # Cancel game
        game.cancel()

        return False

    result = game.chat.message(bot_answer)

    # write bot answer
    result = game.save_bot_answer(result)
    logging.info(result)

    return True


def process_message(message: dict):

    # init Game
    game = CityGame(message=message)

    # get current city
    city = message['message']['text']

    # Checing bot
    if message['message']['from']['is_bot']:
        return False

    # dirty words
    if helpers.check_obscenity(city):
        game.chat.message('Не ругайся матом тупая ты скотина!')
        return False

    # game exists
    if not game.exists():
        game.chat.message('Вы еще не начали, нажмите /start чтобы поиграть в города!')
        return False

    # get last answer
    last_answer = game.get_last_answer()

    # check prevoius answers
    if game.is_answered_city():
        game.chat.message(f'Город {city} уже использовали в ответах!')
        return False

    # check last symbol from last answer
    if not helpers.is_word_in_chain(last_answer['message'], city):
        err_msg = f"Ваш город {message['message']['text']} не начинается с последнего символа предыдущего города {last_answer['message']} из ответов"
        game.chat.message(err_msg)
        return False

    # city exists
    if not cities.city_exists(city):
        game.chat.message(f'Города {city} не существует!')
        return False

    # save user answer
    game.save_user_answer()

    # send bot answer
    send_bot_answer(message)
