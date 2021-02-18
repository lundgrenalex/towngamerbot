telegram_key = ''
store_dir = './tmp/'
cities_dir = './data/'

try:
    from config_local import *  # noqa
except ImportError:
    pass
