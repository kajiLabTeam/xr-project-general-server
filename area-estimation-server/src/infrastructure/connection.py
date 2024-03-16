from psycopg2 import connect
from psycopg2.extensions import connection

from config.env import PostgresEnv


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
