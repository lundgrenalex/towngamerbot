import random
from typing import List

from src.drivers import mongo
from src.domain.city import City


class CityRepositoRy:

    def __init__(self):
        self.db = mongo.connect()

    def add_indexes(self):
        return self.db.bot.cities.create_index('city')

    def drop_all(self) -> object:
        return self.db.bot.cities.delete_many({})

    def insert(self, cities: List[City]):
        return self.db.bot.cities.insert_many([city.__dict__ for city in cities])

    def random(self):
        cities = self.db.bot.cities.distinct('city')
        return random.choice([c for c in cities])

    def get_all(self):
        cities = self.db.bot.cities.distinct('city')
        return [c.lower() for c in cities]

    def exists(self, city: str) -> bool:
        city = self.db.bot.cities.find_one({'city': {
            '$regex': f'^{city}$',
            '$options': 'i'
        }})
        return True if city else False
