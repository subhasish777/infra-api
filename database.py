import psycopg2
import os

def get_connection():
    # Uses environment variables so you don't hardcode credentials in Git
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "infradb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "password")
    )