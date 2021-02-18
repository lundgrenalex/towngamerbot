from lib import commands
from lib import helpers
from lib.storage import cities, game
import logging
from lib import telegram
from config import telegram_key


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

    bot_answer = game.get_new_answer(message)
    if not bot_answer:

        # Get score for username
        score = game.get_score(chat_id)
        username = telegram.get_chat(
            chat_id,
            bot_token=telegram_key)['result']['username']

        telegram.send_message(
            message['message']['chat']['id'],
            message=helpers.render_template('winner', username, score),
            bot_token=telegram_key)

        # Cancel game
        game.cancel(chat_id)

        return False

    result = telegram.send_message(
        message['message']['chat']['id'],
        message=bot_answer,
        bot_token=telegram_key)
    logging.info(result)

    # write bot answer
    result = game.save_bot_answer(result)
    logging.info(result)

    return True

    pass

def process_message(message: dict):

    # get chat_id
    chat_id = message['message']['chat']['id']

    # get current city
    city = message['message']['text']

    # Checing bot
    if message['message']['from']['is_bot']:
        return False

    # dirty words
    if helpers.check_obscenity(city):
        telegram.send_message(
            chat_id,
            message='Не ругайся матом тупая ты скотина!',
            bot_token=telegram_key)
        return False

    # game exists
    if not game.exists(message):
        telegram.send_message(
            chat_id,
            message='Вы еще не начали, нажмите /start чтобы поиграть в города!',
            bot_token=telegram_key)
        return False

    # get last answer
    last_answer = game.get_last_answer(message)

    # check prevoius answers
    if game.is_answered_city(message):
        result = telegram.send_message(
            chat_id,
            message=f'Город {city} уже использовали в ответах!',
            bot_token=telegram_key)
        return False

    # check last symbol from last answer
    if not helpers.is_word_in_chain(last_answer['message'], message['message']['text']):
        err_msg = f"Ваш город {message['message']['text']} не начинается с последнего символа предыдущего города {last_answer['message']} из ответов"
        result = telegram.send_message(
            chat_id,
            message=err_msg,
            bot_token=telegram_key)
        return False

    # city exists
    if not cities.city_exists(city):
        result = telegram.send_message(
            chat_id,
            message=f'Города {city} не существует!',
            bot_token=telegram_key)
        return False

    print('I"m here!')

    # save user answer
    game.save_user_answer(message)

    # send bot answer
    send_bot_answer(message)
