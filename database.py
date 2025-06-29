# database.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="riftcards",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
