from lib import store

user_store = store.get('12243234234')
print("User Store: \n", user_store)

cities_store = store.get_cities()
print("Cities Store: \n", cities_store)
