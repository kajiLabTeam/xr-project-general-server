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


class MinioEnv:
    def __init__(self):
        self.__service_name = "s3"
        self.__endpoint = os.getenv("MINIO_ENDPOINT")
        self.__access_key = os.getenv("MINIO_ACCESS_KEY")
        self.__secret_key = os.getenv("MINIO_SECRET_KEY")
        self.__region = os.getenv("MINIO_REGION")

    def get_service_name_of_private_value(self):
        return self.__service_name

    def get_endpoint_of_private_value(self):
        return self.__endpoint

    def get_access_key_of_private_value(self):
        return self.__access_key

    def get_secret_key_of_private_value(self):
        return self.__secret_key

    def get_region_of_private_value(self):
        return self.__region
