import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()


def create_tables():

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS mac_ip_pairs (
                mac_address VARCHAR(255),
                ip_address VARCHAR(255) NOT NULL
            );
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS computers (
                computer_name VARCHAR(255) PRIMARY KEY,
                mac_address VARCHAR(255) NOT NULL
            );
        ''')
    conn.commit()
