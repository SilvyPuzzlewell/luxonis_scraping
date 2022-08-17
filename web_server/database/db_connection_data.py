import os


def get_db_connect_dict():
    env = os.environ
    db = {
        "user": env["DB_USER"],
        "host": env["DB_HOST"],
        "database": env["DB_NAME"],
        "password": env["DB_PASSWORD"],
        "port": env["DB_PORT"]
    }
    return db

def get_db_connect_dict_test():
    db = {
        "user": 'postgres',
        "host": 'localhost',
        "database": 'realities',
        "password": 'postgres',
        "port": 5342
    }
    return db