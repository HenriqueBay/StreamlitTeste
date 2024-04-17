import os
from psycopg2 import connect
from dotenv import load_dotenv

load_dotenv()

class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = connect(
                database = os.getenv('DATABASE'),
                user = os.getenv('DB_USER'),
                password = os.getenv('PASSWORD'),
                host = os.getenv('HOST_LOCAL'),
                port = os.getenv('LOCAL_PORT')
            )
        return cls._instance

