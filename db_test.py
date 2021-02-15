import json
from lib.storage import mongo

db = mongo.connect()

db.bot.cities.remove({})

with open('./data/cities.json', 'r') as city_file:
    fixed_cities = []
    cities = json.loads(city_file.read())
    for city in cities:
        city['city'] = (city['city']).lower()
        fixed_cities.append(city)
    db.bot.cities.insert_many(fixed_cities)

cities = db.bot.cities.distinct('city')
cities = [c.lower() for c in cities]
print(cities)
