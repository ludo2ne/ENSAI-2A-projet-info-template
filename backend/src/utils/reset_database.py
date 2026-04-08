import logging
import os
from unittest import mock

import dotenv

from dao.db_connection import DBConnection
from service.player_service import PlayerService
from utils.log_decorator import log
from utils.singleton import Singleton


class ResetDatabase(metaclass=Singleton):
    """
    Database reset utility
    """

    @log
    def run(self, test_dao=False):
        """Run the database reset
        If test_dao=True: reset test data
        """
        if test_dao:
            mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": "project_test_dao"}).start()
            pop_data_path = "data/pop_db_test.sql"
        else:
            pop_data_path = "data/pop_db.sql"

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        with open("data/init_db.sql", encoding="utf-8") as init_db_file:
            init_db_as_string = init_db_file.read()

        with open(pop_data_path, encoding="utf-8") as pop_db_file:
            pop_db_as_string = pop_db_file.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
        except Exception as e:
            logging.info(e)
            raise

        # Apply password hashing to all players
        player_service = PlayerService()
        for p in player_service.find_all(include_password=True):
            player_service.update(p)

        return True


if __name__ == "__main__":
    ResetDatabase().run()
    ResetDatabase().run(True)
