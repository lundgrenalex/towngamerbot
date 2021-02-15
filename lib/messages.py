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

def bot_answer(message: dict):

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
        bot_token=telegram_key
    )
    logging.info(result)

    # write bot answer
    result = game.save_bot_answer(result)
    logging.info(result)

    return True

    pass

def process_message(message: dict):

    # BUGFIX: to lower text
    message['message']['text'] = (message['message']['text']).lower()

    # BUGFIX: FIX Ёё
    message['message']['text'] = (message['message']['text']).replace('ё', 'е')

    # get chat_id
    chat_id = message['message']['chat']['id']

    # dirty words
    if helpers.check_obscenity(message['message']['text']):
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

    # get last message
    last_answer = game.get_last_answer(message)
    if not last_answer:
        logging.warning(f'Не найден последний ответ в чате: {chat_id}')
        return False

    # last_answer uid =! uid
    if last_answer['user_id'] == message['message']['from']['id']:
        return bot_answer(message)

    # check last symbol from last answer
    if not helpers.is_word_in_chain(last_answer['message'], message['message']['text']):
        err_msg = f"Ваш город {message['message']['text']} не начинается с последнего символа предыдущего города {last_answer['message']} из ответов"
        result = telegram.send_message(
            chat_id,
            message=err_msg,
            bot_token=telegram_key
        )
        logging.warning(err_msg)
        return False

    # get current city
    city = (message['message']['text']).lower()

    # Get city list
    all_cities = cities.get_all()

    # Check if city exists
    if city not in all_cities:
        result = telegram.send_message(
            chat_id,
            message=f'Города {city} не существует!',
            bot_token=telegram_key
        )
        logging.debug(f'Wrong city: {city}')
        return False

    # check prevoius answers
    if game.is_answered_city(message):
        result = telegram.send_message(
            chat_id,
            message=f'Город {city} уже использовали в ответах!',
            bot_token=telegram_key
        )
        logging.info(f'Answered city: {city}')
        return False

    # save user answer
    if not game.save_user_answer(message):
        logging.info(f'Can\'t write city to database: {city}')
        return False

    # get bot answer
    return bot_answer(message)
