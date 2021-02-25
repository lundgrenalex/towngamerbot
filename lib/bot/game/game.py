import pymongo
import random
from lib.storage import mongo
from .exceptions import GameError
from lib import helpers
import time
import re
import logging

class CityGame:

    def __init__(self, message:dict):
        self.message = message
        self.db = mongo.connect()

    def exists(self,):
        return self.db.bot.game.find_one({
            'chat_id': self.message['message']['chat']['id'],
        })

    def save_bot_answer(self, answer: dict):
        return self.db.bot.game.insert_one({
            'date': time.time(),
            'chat_id': answer['result']['chat']['id'],
            'user_id': answer['result']['from']['id'],
            'message': answer['result']['text'],
        })

    def save_user_answer(self):
        return self.db.bot.game.insert_one({
            'date': time.time(),
            'chat_id': self.message['message']['chat']['id'],
            'user_id': self.message['message']['from']['id'],
            'message': self.message['message']['text'],
        })

    def cancel(self):
        chat_id = self.message['message']['chat']['id']
        return self.db.bot.game.remove({'chat_id': chat_id})

    def is_answered_city(self):
        result = self.db.bot.game.find_one({
            'chat_id': self.message['message']['chat']['id'],
            'message': {
                '$regex': f"{self.message['message']['text']}",
                '$options' : 'i'
            }
        })
        return result

    def get_last_answer(self):
        messages = self.db.bot.game.find({
            'chat_id': self.message['message']['chat']['id'],
        }, {'_id': False}).sort([('date', pymongo.DESCENDING)]).limit(1)
        try:
            return [m for m in messages][0]
        except IndexError:
            return False

    def get_new_answer(self):
        chat_id = self.message['message']['chat']['id']
        city_name = helpers.normalize_city_name(self.message['message']['text'])

        last_simbol = list(city_name)[-1:][0]
        cities = self.db.bot.cities.find({
            'city': {
                '$regex': f'^{last_simbol}',
                '$options' : 'i'
        }}).sort([('population', pymongo.DESCENDING)])

        # get answered cities
        answered_cities = self.db.bot.game.find({'chat_id': chat_id})
        answered_cities = [c['message'].lower() for c in answered_cities]

        for city in cities:
            if city['city'].lower() in answered_cities:
                continue
            return city['city']

    def get_hint(self):

        if not self.exists():
            message="Game doesn't exists!"
            # raise GameError(message="Game doesn't exists!")
            logging.error(message)
            return

        return 'Game exists!'

    def get_score(self) -> int:
        chat_id = self.message['message']['chat']['id']
        score = 0
        answers = [a['message'] for a in self.db.bot.game.find({'chat_id': chat_id})]

        # get keys
        for a in answers:
            score += (1 / self.db.bot.cities.count({
                'city': {'$regex': f'^{a[0]}', '$options' : 'i'}}))

        # return real score
        return int(score * 1000)
