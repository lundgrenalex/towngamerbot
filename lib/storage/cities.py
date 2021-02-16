import random
from lib.storage import mongo


def get_random():
    db = mongo.connect()
    cities = db.bot.cities.distinct('city')
    cities = [c.lower() for c in cities]
    return random.choice(cities)

def get_all():
    db = mongo.connect()
    cities = db.bot.cities.distinct('city')
    return [c.lower() for c in cities]

def city_exists(city: str) -> bool:
    db = mongo.connect()
    city = db.bot.cities.find_one({'city': {
        '$regex': f'^{city}$',
        '$options' : 'i'
    }})
    return True if city else False
