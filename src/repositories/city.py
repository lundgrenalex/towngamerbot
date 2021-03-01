import random
import logging
from src.drivers import mongo


class City:

    def __init__(self):
        self.db = mongo.connect()

    def random(self):
        cities = self.db.bot.cities.distinct('city')
        return random.choice([c for c in cities])

    def get_all(self):
        cities = self.db.bot.cities.distinct('city')
        return [c.lower() for c in cities]

    def exists(self, city: str) -> bool:
        city = self.db.bot.cities.find_one({'city': {
            '$regex': f'^{city}$',
            '$options' : 'i'
        }})
        return True if city else False
