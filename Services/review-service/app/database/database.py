from mongoengine import connect


class MongoDB():
    def __init__(self, mongo_dsn):
        connect(host=mongo_dsn)
