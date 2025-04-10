import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env.dev")

def get_connection():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        host = os.getenv("DB_HOST"),
        port = os.getent("DB_HOST)")
    )