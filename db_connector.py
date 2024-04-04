import socket
import psycopg2
from psycopg2 import pool
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv('DATABASE')
DB_USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST_LOCAL')  # ou o host do seu banco de dados
PORT = os.getenv('PORT')        # ou a porta do seu banco de dados

# Conecta ao banco de dados PostgreSQL
connection = psycopg2.connect(
    database=DATABASE,
    user=DB_USER,
    password=PASSWORD,
    host=HOST,
    port=7000
)
