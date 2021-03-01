from pymongo import MongoClient


connection = None


def connect(conn_str='mongodb://mongodb:27017', pullSize=1024, **mongo_settings):
    global connection
    if not connection:
        connection = MongoClient(
            conn_str,
            connect=False,
            maxPoolSize=pullSize,
            waitQueueMultiple=10,
            waitQueueTimeoutMS=1000
        )
    return connection
