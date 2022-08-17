# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sys
import time

import psycopg2
import logging

env = os.environ
LOGGING_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d %(message)s')

def get_logger():
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGING_FORMATTER)
    logger.setLevel(env["LOGGING_LEVEL"])
    logger.addHandler(console_handler)
    return logger

logger = logging.getLogger()
logger.setLevel(env["LOGGING_LEVEL"])

class DbConnector:
    def __init__(self, db):
        self.connection_data = db

    def clear_table_flats(self):
        query = "DELETE FROM flats"
        with psycopg2.connect(**self.connection_data) as conn:
            with conn.cursor() as curs:
                curs.execute(query)
                conn.commit()


    def create_table_flats(self):
        query = "CREATE TABLE IF NOT EXISTS flats (user_id SERIAL PRIMARY KEY, title VARCHAR(250), img_url TEXT)"
        logger.debug(f"#########connection info#####\n{self.connection_data}\n###############")
        with psycopg2.connect(**self.connection_data) as conn:
            with conn.cursor() as curs:
                curs.execute(query)
                conn.commit()

    def insert_flat(self, flat):
        query = """
                INSERT INTO flats (title, img_url)
                VALUES
                (%s, %s)
                """
        with psycopg2.connect(**self.connection_data) as conn:
            with conn.cursor() as curs:
                curs.execute(query, flat)
                conn.commit()




class RealityScrapingPipeline:

    def open_spider(self, spider):
        db = {
            "user": env["DB_USER"],
            "host": env["DB_HOST"],
            "database": env["DB_NAME"],
            "password": env["DB_PASSWORD"],
            "port": env["DB_PORT"]
        }
        print("intializing db transfer")
        self.db = DbConnector(db)
        db_working = False
        while not db_working:
            try:
                self.db.create_table_flats()
                logger.info("Flats DB table initalized in case it didn't exist.")
                db_working = True
            except Exception:
                logger.info("Database connection not succesful now, db is still possibly initializing")
                time.sleep(1)
                continue

            try:
                self.db.clear_table_flats()
                logger.info("Data cleared upon new scraping operation")
            except Exception:
                logger.warning("Exception during cleaning old data")




    def process_item(self, item, spider):
        logger.info(f"saving item {item['title']}")
        flats_uploaded = False
        while not flats_uploaded:
            try:
                self.db.insert_flat((item['title'], item['img_url']))
                logger.debug("item succesfully saved")
                flats_uploaded = True
            except Exception as e:
                logger.warning("Uploading flat to db failed! waiting 10s to try again.")
                logger.exception(e)
                time.sleep(10)
        return item





