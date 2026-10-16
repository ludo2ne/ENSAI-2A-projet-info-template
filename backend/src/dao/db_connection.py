import os

import psycopg2
from psycopg2.extras import RealDictCursor

from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    def __init__(self):
        self.__connection = None
        self.__connect()

    def __connect(self):
        """Établit la connexion initiale."""
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
        """
        Retourne la connexion.
        Si la connexion est fermée, elle tente de se reconnecter.
        """
        if self.__connection is None or self.__connection.closed != 0:
            self.__connect()
        return self.__connection

    def ensure_connection(self):
        """Vérifie activement si la connexion est valide via une requête simple."""
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT 1")
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.__connect()
