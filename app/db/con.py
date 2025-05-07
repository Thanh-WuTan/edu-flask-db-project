import mysql.connector
from ..config import Config

def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT
    )