import json
from pymongo import MongoClient, ASCENDING, DESCENDING

db = MongoClient('mongodb://mongodb:27017')

# CITIES
db.bot.cities.delete_many({})

def get_unique_cities(cities: list) -> list:
    unique_cities = []
    for c in cities:
        if c not in unique_cities:
            unique_cities.append(c)
    return unique_cities

def prepare_cities(cities: list) -> list:
    cities = [c['city'] for c in cities]
    cities = get_unique_cities(cities)
    return [{'city': c} for c in cities]

with open('./data/cities.json', 'r') as city_file:
    fixed_cities = []
    cities = json.loads(city_file.read())
    db.bot.cities.insert_many(prepare_cities(cities))

cities = db.bot.cities.distinct('city')
print(cities)

# GAME
result = []

result.append(db.bot.game.create_index('date'))
result.append(db.bot.game.create_index('chat_id'))
result.append(db.bot.game.create_index('user_id'))
result.append(db.bot.game.create_index('message'))
result.append(db.bot.cities.create_index('city'))

print(result)
