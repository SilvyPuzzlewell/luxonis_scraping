import configparser

import psycopg2

from database.db_connection_data import get_db_connect_dict


class DbConnector:
    def __init__(self, connection_data):

        self.connection_data = connection_data



    def load_flats(self):
        query = "SELECT title, img_url FROM flats"
        with psycopg2.connect(**self.connection_data) as conn:
            with conn.cursor() as curs:
                curs.execute(query)
                ret = curs.fetchall()
        return ret
