from pymongo import MongoClient, ASCENDING, DESCENDING

db = MongoClient('mongodb://localhost:27017')

# CITIES
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

# GAME
result = []

result.append(db.bot.game.create_index('date'))
result.append(db.bot.game.create_index('chat_id'))
result.append(db.bot.game.create_index('user_id'))
result.append(db.bot.game.create_index('message'))

print(result)
