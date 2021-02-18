import pymongo
import random
from lib.storage import mongo
from lib import helpers
import time
import re
import logging


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
        'message': answer['result']['text'],
    })

def save_user_answer(message: dict):
    db = mongo.connect()
    return db.bot.game.insert_one({
        'date': time.time(),
        'chat_id': message['message']['chat']['id'],
        'user_id': message['message']['from']['id'],
        'message': message['message']['text'],
    })

def cancel(chat_id: int):
    db = mongo.connect()
    return db.bot.game.remove({'chat_id': chat_id})

def is_answered_city(message: dict):
    db = mongo.connect()
    result = db.bot.game.find_one({
        'chat_id': message['message']['chat']['id'],
        'message': {
            '$regex': f"{message['message']['text']}",
            '$options' : 'i'
        }
    })
    return result

def get_last_answer(message: dict):
    db = mongo.connect()
    messages = db.bot.game.find({
        'chat_id': message['message']['chat']['id'],
    }, {'_id': False}).sort([('date', pymongo.DESCENDING)]).limit(1)
    return [m for m in messages][0]

def get_new_answer(message: dict):
    db = mongo.connect()
    chat_id = message['message']['chat']['id']
    city_name = helpers.normalize_city_name(message['message']['text'])

    last_simbol = list(city_name)[-1:][0]
    cities = db.bot.cities.find({
        'city': {
            '$regex': f'^{last_simbol}',
            '$options' : 'i'
    }}).sort([('population', pymongo.DESCENDING)])

    # get answered cities
    answered_cities = db.bot.game.find({'chat_id': chat_id})
    answered_cities = [c['message'].lower() for c in answered_cities]

    for city in cities:
        if city['city'].lower() in answered_cities:
            continue
        return city['city']

def get_hint(message: dict):
    db = mongo.connect()
    city_name = get_new_answer(message)
    city_info = db.bot.cities.find_one({'city': city_name})
    hint = f"Город из {len(city_info['city'])} букв, располежнный в {city_info['state']} {city_info['region']} региона с население из {city_info['population']} человек"
    return hint

def get_score(chat_id: int) -> int:
    db = mongo.connect()
    score = 0
    answers = [a['message'] for a in db.bot.game.find({'chat_id': chat_id})]

    # get keys
    for a in answers:
        score += (1 / db.bot.cities.count({
            'city': {'$regex': f'^{a[0]}', '$options' : 'i'}}))

    # return real score
    return int(score * 1000)
