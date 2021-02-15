db.cities.findOne({'$and': [
    {'city': {'$regex': '^к'}},
    {'city': {'$nin': ['омск', 'черкизово']}}
]})

db.cities.findOne({'$and': [
    {'city': {'$nin': ['омск', 'черкизово']}}
]})

db.cities.findOne({'$and': [
    {'city': {'$regex': '/^к/'}},
]})
