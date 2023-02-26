from peewee import *

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

database = MySQLDatabase(DATABASE_NAME, user=DATABASE_USER,
                         password=DATABASE_PASSWORD,
                         host=DATABASE_HOST, port=3306)
