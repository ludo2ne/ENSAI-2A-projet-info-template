import os

import psycopg2
from psycopg2.extras import RealDictCursor

from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Database connection class.
    It allows you to open only a single connection.
    """

    def __init__(self):
        """Open connection"""

        self.__connection = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            options=f"-c search_path={os.environ['POSTGRES_SCHEMA']}",
            cursor_factory=RealDictCursor,
        )

    @property
    def connection(self):
        return self.__connection
