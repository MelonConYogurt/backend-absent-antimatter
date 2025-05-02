import os
import psycopg2
from dotenv import load_dotenv


class Connection:
    def __init__(self):
        load_dotenv()

    def load_env(self):
        return {
            "host": os.getenv("PGHOST"),
            "dbname": os.getenv("PGDATABASE"),
            "user": os.getenv("PGUSER"),
            "password": os.getenv("PGPASSWORD"),
        }

    def conn(self):
        try:
            config = self.load_env()
            conn = psycopg2.connect(**config)
            if conn:
                return conn
        except psycopg2.Error as e:
            print(e)
            raise
