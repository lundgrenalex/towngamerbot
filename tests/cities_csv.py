

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
