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

    chat_id = message['message']['chat']['id']
    if game.exists(message):
        telegram.send_message(
            chat_id,
            message='Вы еще не закончили последнюю игру, нажмите /stop или говорите город!',
            bot_token=telegram_key)
        return

    # Get random city
    city = cities.get_random()

    # send_message
    telegram.send_message(
        chat_id,
        message=city.capitalize(),
        bot_token=telegram_key
    )

    # write bot answer
    game.save_bot_answer(result)
    
    return
