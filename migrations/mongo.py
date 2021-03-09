from src.domain.city import City
from src.repositories.city import CityRepositoRy
from src.repositories.game import GameRepository

city_store = CityRepositoRy()
game_store = GameRepository()

# Remove old cities
city_store.drop_all()

# add_indexes to game, city stores
game_store.add_indexes()
city_store.add_indexes()

with open('./data/cities.csv', 'r') as city_file:
    city_lines = city_file.readlines()
    cities = []
    for cl in city_lines:
        cl = cl.replace('\n', '').split(';')
        cities.append(City(city=cl[0], state=cl[1], region=cl[2], population=cl[3]))
    city_store.insert(cities)
