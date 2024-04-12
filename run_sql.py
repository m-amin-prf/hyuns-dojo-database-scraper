import mysql.connector
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()


def init_db():  # Initialise Database with mysql.connector
    return mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_ID"))


db = init_db()


def get_cursor():  # Get cursor if one doesn't already exist
    global db
    try:
        db.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        # reconnect your cursor as you did in __init__ or wherever
        db = init_db()
    return db.cursor()
