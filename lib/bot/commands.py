import re
import json
import logging
from lib import helpers
from .game import cities
from .game import CityGame
from lib.messages.chat import Chat


def process(message: dict):
    start(message)
    stop(message)
    hint(message)

def stop(message: dict) -> None:

    if not re.search(r'\/stop', message['message']['text']):
        return

    g = CityGame(message=message)
    chat = Chat(chat_id=message['message']['chat']['id'])

    if not g.exists():
        chat.message('Вы еще не начали, нажмите /start чтобы начать играть в города!')
        return

    # Get score for username and send message
    score = int(g.get_score() * 0.75)
    chat.message(helpers.render_template(
        'stopped', message['message']['chat']['username'], score))

    # Cancel game
    g.cancel()


def start(message: dict):

    if not re.search(r'\/start', message['message']['text']):
        return

    g = CityGame(message=message)
    chat = Chat(chat_id=message['message']['chat']['id'])

    if g.exists():
        chat.message('Вы еще не закончили последнюю игру, нажмите /stop или говорите город!')
        return

    # Get random city
    city = cities.get_random()

    # send_message
    result = chat.message(city)
    logging.info(result)

    # write bot answer
    result = g.save_bot_answer(result)
    logging.info(result)

    return

def hint(message: dict):

    if not re.search(r'\/hint', message['message']['text']):
        return

    g = CityGame(message=message)
    chat = Chat(chat_id=message['message']['chat']['id'])

    return chat.message(g.get_hint())
