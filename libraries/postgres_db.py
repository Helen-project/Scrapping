"""DB module."""
import datetime
import subprocess
import psycopg2

from libraries import logger


class PostgresSql:
    """Class object for DB."""

    def __init__(self, dbname, user, password, host):
        """Functions initialise the class."""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.connection = None
        self.__connect_to_db()

    def __connect_to_db(self):
        """Functions for connection to DB."""
        self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)

    def __close_connection(self):
        """Functions for closing connection to DB."""
        self.connection.close()

    def create_db(self):
        """Functions for creating DB."""
        self.connection.autocommit = True
        cur = self.connection.cursor()
        cur.execute(f"CREATE DATABASE {self.dbname}")
        self.connection.commit()
        cur.close()

    def create_table(self, table_name, columns):
        """Functions for creating table in DB."""
        cursor = self.connection.cursor()
        col = ""
        for column, col_type in columns.items():
            col += f"{column} {col_type}, "

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255),
                title VARCHAR(255),
                price_usd INT,
                odometer INT,
                user_name VARCHAR(255),
                phone_number INT,
                image_url VARCHAR(255),
                image_count INT,
                car_number VARCHAR(255),
                car_vin VARCHAR(255),
                datetime_found TIMESTAMP
            )
        """
        )
        self.connection.commit()
        cursor.close()

    def insert_data(self, table_name, data_df):
        """Functions for insert data to table."""
        logger.info("Insert data to DB.")
        cursor = self.connection.cursor()
        columns_name = (
            "url, title, price_usd, odometer, user_name, phone_number, image_url, "
            "image_count, car_number, car_vin, datetime_found"
        )
        cursor.executemany(
            f"""
            INSERT INTO {table_name} ({columns_name})
            SELECT * FROM (VALUES %s) as n ({columns_name})
            WHERE NOT EXISTS (
                SELECT 1 FROM {table_name} e WHERE e.url = n.url
            )
            """,
            [(row,) for row in data_df.itertuples(index=False)],
        )

        self.connection.commit()
        cursor.close()

    def __del__(self):
        """Functions for closing connection when object will be removed from memory."""
        self.__close_connection()

    def create_dump_file(self, dump_file_path=f"dumps/.dump_{datetime.datetime.now().strftime('%Y-%m-%d')}"):
        """Functions for creating dump file."""
        try:
            pg_dump_cmd = ["pg_dump", "-U", self.user, "-d", self.dbname, "-f", dump_file_path]
            subprocess.run(pg_dump_cmd, check=True)
            logger.info(f"Dump file created successfully: {dump_file_path}")
        except subprocess.CalledProcessError as e:
            logger.info(f"Error creating dump file: {e}")
