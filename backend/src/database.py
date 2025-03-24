import psycopg2
from src.config import DATABASE_URL

def get_database_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connection DB Posgtresql success")
        return conn
    except psycopg2.Error as e:
        print(f"Connection DB Posgtresql error: {e}")
        raise Exception("Connection error")
