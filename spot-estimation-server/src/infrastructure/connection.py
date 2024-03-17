from typing import Any

import boto3  # type: ignore
from config.env import MinioEnv, PostgresEnv
from psycopg2 import connect
from psycopg2.extensions import connection


class DBConnection:
    @staticmethod
    def connect() -> connection:
        env = PostgresEnv()
        return connect(
            host=env.get_host_of_private_value(),
            port=env.get_port_of_private_value(),
            user=env.get_user_of_private_value(),
            password=env.get_password_of_private_value(),
            dbname=env.get_database_of_private_value(),
        )


class MinioConnection:
    @staticmethod
    def connect() -> Any:
        env = MinioEnv()
        return boto3.client(  # type: ignore
            service_name=env.get_service_name_of_private_value(),
            endpoint_url=env.get_endpoint_of_private_value(),
            aws_access_key_id=env.get_access_key_of_private_value(),
            aws_secret_access_key=env.get_secret_key_of_private_value(),
            region_name=env.get_region_of_private_value(),
        )
