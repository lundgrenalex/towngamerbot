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
