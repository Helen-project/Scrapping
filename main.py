"""Main module."""
import os
import time

import schedule
from dotenv import load_dotenv

from libraries import logger
from libraries.postgres_db import PostgresSql
from libraries.sites.site_auto import AutoRia

load_dotenv()
TIME_RUN = os.getenv("TIME_RUN")


def main():
    """Main function."""
    logger.info("Start process AutoRia Scrapping.")
    db_name = os.getenv("DB_NAME")
    db_table_name = os.getenv("TABLE_NAME")
    db_user_name = os.getenv("DB_USER_NAME")
    db_user_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    auto_ria = AutoRia()
    cars_data = auto_ria.get_cars_data()
    db = PostgresSql(db_name, db_user_name, db_user_password, db_host)
    df_data = [car.convert_to_db() for car in cars_data]
    db.insert_data(db_table_name, df_data)
    db.create_dump_file()
    logger.info("Finish the process AutoRia Scrapping.")


if __name__ == "__main__":
    schedule.every().day.at(TIME_RUN).do(main)

    while True:
        schedule.run_pending()
        time.sleep(50)
