import logging
import pymongo

from src.libs import helpers
from src.drivers import mongo
from src.repositories.chat import Chat
# from src.repositories.exceptions import GameError


class CityGame:

    def __init__(self, message: dict):
        self.message = message
        self.db = mongo.connect()
        self.chat = Chat(chat_id=message['message']['chat']['id'])

    def exists(self):
        return self.db.bot.game.find_one({
            'chat_id': self.message['message']['chat']['id'],
        })

    def cancel(self):
        chat_id = self.message['message']['chat']['id']
        return self.db.bot.game.remove({'chat_id': chat_id})

    def is_answered_city(self):
        result = self.db.bot.game.find_one({
            'chat_id': self.message['message']['chat']['id'],
            'message': {
                '$regex': f"{self.message['message']['text']}",
                '$options': 'i'
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
                '$options': 'i'}}).sort([
                    ('population', pymongo.DESCENDING)
                ])

        # get answered cities
        answered_cities = self.db.bot.game.find({'chat_id': chat_id})
        answered_cities = [c['message'].lower() for c in answered_cities]

        for city in cities:
            if city['city'].lower() in answered_cities:
                continue
            return city['city']

    def get_hint(self):

        if not self.exists():
            message = "Game doesn't exists!"
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
                'city': {'$regex': f'^{a[0]}', '$options': 'i'}}))

        # return real score
        return int(score * 1000)
