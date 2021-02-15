import re
import json
from lib import telegram, helpers
from config import telegram_key
from lib.storage import mongo, game, cities
import logging

def process(message: dict):
    start(message)
    stop(message)

def stop(message: dict):

    if not re.search(r'\/stop', message['message']['text']):
        return

    # get user meta
    chat_id = message['message']['chat']['id']
    username = message['message']['chat']['username']

    if not game.exists(message):
        telegram.send_message(
            chat_id,
            message='Вы еще не начали, нажмите /start чтобы начать играть в города!',
            bot_token=telegram_key)
        return False

    # Get score for username
    score = int(game.get_score(chat_id) * 0.75)

    telegram.send_message(
        chat_id,
        message=helpers.render_template('stopped', username, score),
        bot_token=telegram_key)

    # Cancel game
    game.cancel(chat_id)

    return True

def start(message: dict):

    if not re.search(r'\/start', message['message']['text']):
        return

    # Get random city
    city = cities.get_random()

    # send_message
    result = telegram.send_message(
        message['message']['chat']['id'],
        message=city.capitalize(),
        bot_token=telegram_key
    )
    logging.info(result)

    # write bot answer
    result = game.save_bot_answer(result)
    logging.info(result)

    return
