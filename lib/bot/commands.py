import re
import json
import logging
from lib import helpers
from lib.game import cities
from lib.game import CityGame


def process(message: dict):
    start(message)
    stop(message)
    hint(message)

def stop(message: dict) -> None:

    if not re.search(r'\/stop', message['message']['text']):
        return

    game = CityGame(message=message)

    if not game.exists():
        game.chat.message('Вы еще не начали, нажмите /start чтобы начать играть в города!')
        return

    # Get score for username and send message
    score = int(game.get_score() * 0.75)
    game.chat.message(helpers.render_template(
        'stopped', message['message']['chat']['username'], score))

    # Cancel game
    game.cancel()


def start(message: dict):

    if not re.search(r'\/start', message['message']['text']):
        return

    game = CityGame(message=message)

    if game.exists():
        game.chat.message('Вы еще не закончили последнюю игру, нажмите /stop или говорите город!')
        return

    # Get random city
    city = cities.get_random()

    # send_message
    result = game.chat.message(city)
    logging.info(result)

    # write bot answer
    result = game.save_bot_answer(result)
    logging.info(result)

    return

def hint(message: dict):

    if not re.search(r'\/hint', message['message']['text']):
        return

    game = CityGame(message=message)

    return game.chat.message(game.get_hint())
