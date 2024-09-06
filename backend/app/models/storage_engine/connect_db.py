"""Module for mysql to create database if not exist"""

import os

import MySQLdb  # type: ignore
from dotenv import load_dotenv

load_dotenv()


class ConnectMysqlDB:
    """Connect to MySQL database and create it if it does not exist."""

    __has_connected = False
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PWD = os.getenv("MYSQL_PWD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DB = os.getenv("MYSQL_DB")

    def __init__(self):
        """Instantiate a DBStorage object and create \
            the database if necessary."""
        print(f"Connecting to MySQL host: {ConnectMysqlDB.MYSQL_HOST}")
        ConnectMysqlDB.create_database_if_not_exists()

    @classmethod
    def create_database_if_not_exists(cls):
        """Create the database if it does not exist."""
        count = 0
        while count < 10:
            try:
                conn = MySQLdb.connect(
                    host=ConnectMysqlDB.MYSQL_HOST,
                    user=ConnectMysqlDB.MYSQL_USER,
                    passwd=ConnectMysqlDB.MYSQL_PWD,
                )
                cursor = conn.cursor()
                cursor.execute(
                    f"CREATE DATABASE IF NOT\
                                EXISTS {ConnectMysqlDB.MYSQL_DB}"
                )
                conn.commit()
                conn.close()
                ConnectMysqlDB.__has_connected = True
                print(f"Database {ConnectMysqlDB.MYSQL_DB} ensured.")
                break
            except MySQLdb.MySQLError as e:
                print(
                    f"Failed to connect or create database: {e}, \
                      attempt {count + 1}"
                )
                count += 1
                if count >= 10:
                    print(
                        "Max retries reached. Could not \
                          establish a connection."
                    )

    @staticmethod
    def has_connected():
        return ConnectMysqlDB.__has_connected
