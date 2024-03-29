import os

from dotenv import load_dotenv

load_dotenv()


class PostgresEnv:
    def __init__(self):
        self.__host = os.getenv("POSTGRES_HOST")
        self.__port = os.getenv("POSTGRES_PORT")
        self.__database = os.getenv("POSTGRES_DB")
        self.__user = os.getenv("POSTGRES_USER")
        self.__password = os.getenv("POSTGRES_PASSWORD")

    def get_host_of_private_value(self):
        return self.__host

    def get_port_of_private_value(self):
        return self.__port

    def get_database_of_private_value(self):
        return self.__database

    def get_user_of_private_value(self):
        return self.__user

    def get_password_of_private_value(self):
        return self.__password
