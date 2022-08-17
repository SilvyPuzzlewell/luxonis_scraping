import os
import sys
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer

from database.db_connection_data import get_db_connect_dict
from database.db_connector import DbConnector
import logging

env = os.environ
LOGGING_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d %(message)s')
NUMBER_OF_FLATS = 500
MAX_ATTEMPTS = 5

def get_logger():
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGING_FORMATTER)
    logger.setLevel(env["LOGGING_LEVEL"])
    logger.addHandler(console_handler)
    return logger

def read_html_template(path):
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

def get_flats_from_db():
    flats = []
    load_all_500_attempts_counter = 0
    while len(flats) < NUMBER_OF_FLATS and load_all_500_attempts_counter < MAX_ATTEMPTS:
        try:
            flats = DbConnector(get_db_connect_dict()).load_flats()
        except Exception as e:
            logger.warning("Database connection not succesful!")
            logger.exception(e)
            time.sleep(1)
            continue
        if not flats:
            logger.warning("No flats loaded from db!")
            time.sleep(5)
        elif len(flats) < NUMBER_OF_FLATS and load_all_500_attempts_counter < MAX_ATTEMPTS:
            logger.warning("Not all 500 flats loaded!")
            load_all_500_attempts_counter += 1
            time.sleep(5)


    if load_all_500_attempts_counter == MAX_ATTEMPTS:
        logger.warning(f"All allowed attempts to load the expected {NUMBER_OF_FLATS} "
                       f"flats failed, showing {len(flats)} flats.")
    if len(flats) > 500:
        logger.warning(f"More than expected {NUMBER_OF_FLATS} "
                       f"flats loaded from DB, showing first {NUMBER_OF_FLATS} flats.")
    logger.debug(f"###example flat###\n{flats[0]}####")
    return flats


class PythonServer(SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/':
            logger.info(f"Request to load flat info received.")
            html_path = './templates/show_flats.html'
            file = read_html_template(html_path)
            logger.info(f"Loading flats from db.")
            flats = get_flats_from_db()

            logger.info(f"{len(flats)} flats loaded on local server.")

            def create_div(title, img_url):
                title = title.replace("m2", "m<sup>2</sup>")
                div = f"<div>" \
                      f"<p>{title}</p>" \
                      f"<img src='{img_url}'>" \
                      f"</div>"
                return div

            content = ""
            for flat_info in flats[:NUMBER_OF_FLATS]:
                content += create_div(*flat_info)
            file = file.replace("{{flats}}", content)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

if __name__ == "__main__":
    logger = get_logger()
    logger.info("SERVER SCRIPT STARTED")
    host_name = env["SERVER_HOST"]
    port = int(env["SERVER_PORT"])
    server = HTTPServer((host_name, port), PythonServer)
    logger.info(f"Server started at http://{host_name}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        logger.info("Server stopped succesfully")
        sys.exit(0)
