import json
from pymongo import MongoClient, ASCENDING, DESCENDING

db = MongoClient('mongodb://mongodb:27017')

# CITIES
db.bot.cities.delete_many({})

with open('./data/cities.csv', 'r') as city_file:
    city_lines = city_file.readlines()
    cities = []
    for cl in city_lines:
        cl = cl.replace('\n', '').split(';')
        city = {
            'city': cl[0],
            'state': cl[1],
            'region': cl[2],
            'population': cl[3],
        }
        cities.append(city)
    db.bot.cities.insert_many(cities)

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
