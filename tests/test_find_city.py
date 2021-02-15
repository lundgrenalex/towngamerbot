from lib.storage import mongo


db = mongo.connect()
answer = db.bot.cities.find_one({'$and': [
    {'city': {'$regex': '^к', '$options' : 'i'}},
    # {'city': {'$nin': last_answers}}
]})

print(answer)
