import pymongo
import random
from lib.storage import mongo
from lib import helpers
import time
import re


def exists(message: dict):
    db = mongo.connect()
    return db.bot.game.find_one({
        'chat_id': message['message']['chat']['id'],
    })

def save_bot_answer(answer: dict):
    db = mongo.connect()
    return db.bot.game.insert_one({
        'date': time.time(),
        'chat_id': answer['result']['chat']['id'],
        'user_id': answer['result']['from']['id'],
        'message': answer['result']['text'].lower(),
    })

def save_user_answer(message: dict):
    db = mongo.connect()
    return db.bot.game.insert_one({
        'date': time.time(),
        'chat_id': message['message']['chat']['id'],
        'user_id': message['message']['from']['id'],
        'message': message['message']['text'].lower(),
    })

def cancel(chat_id: int):
    db = mongo.connect()
    return db.bot.game.remove({'chat_id': chat_id})

def is_answered_city(message: dict):
    db = mongo.connect()
    return db.bot.game.find_one({
        'chat_id': message['message']['chat']['id'],
        'message': message['message']['text'].lower(),
    })

def get_last_answer(message: dict):
    db = mongo.connect()
    messages = db.bot.game.find({
        'chat_id': message['message']['chat']['id'],
    }, {'_id': False}).sort([('date', pymongo.DESCENDING)])
    try:
        return [m for m in messages][0]
    except IndexError:
        return False

def get_new_answer(message: dict):
    db = mongo.connect()
    city_name = helpers.normalize_city_name(message['message']['text'])
    last_simbol = list(city_name)[-1:][0]
    last_answers = db.bot.game.find({'chat_id': message['message']['chat']['id']})
    last_answers = [a['message'] for a in last_answers]
    cities = db.bot.cities.find({'$and': [
        {'city': {'$regex': f'^{last_simbol}', '$options' : 'i'}},
        {'city': {'$nin': last_answers}}
    ]})
    try:
        cities = [c['city'] for c in cities]
        return random.choice(cities)
    except (TypeError, IndexError):
        return False

def get_score(chat_id: int) -> int:
    db = mongo.connect()
    score = 0
    answers = [a['message'] for a in db.bot.game.find({'chat_id': chat_id})]

    # get keys
    for a in answers:
        score += (1 / db.bot.cities.count({'city': {'$regex': f'^{a[0]}', '$options' : 'i'}}))

    # return real score
    return int(score * 1000)
