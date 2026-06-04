import logging

from business_object.player import Player
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class PlayerDao(metaclass=Singleton):
    """Class containing methods to access Players in the database."""

    @log
    def create(self, player) -> bool:
        """Create a player in the database.

        Parameters
        ----------
        Player to create

        Returns
        -------
        True if creation is successful, False otherwise
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO player(username, password, elo, email, pokemon_fan) VALUES "
                        "(%(username)s, %(password)s, %(elo)s, %(email)s, %(pokemon_fan)s) "
                        "RETURNING id_player;",
                        {
                            "username": player.username,
                            "password": player.password,
                            "elo": player.elo,
                            "email": player.email,
                            "pokemon_fan": player.pokemon_fan,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            player.id_player = res["id_player"]
            created = True

        return created

    @log
    def find_by_id(self, id_player) -> Player:
        """Find a player by their id

        Parameters
        ----------
        id_player : int
            id of the player to find

        Returns
        -------
        Player matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM player                       "
                        " WHERE id_player = %(id_player)s;   ",
                        {"id_player": id_player},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        player = None
        if res:
            player = Player(
                username=res["username"],
                elo=res["elo"],
                email=res["email"],
                pokemon_fan=res["pokemon_fan"],
                id_player=res["id_player"],
                password=res["password"],
            )

        return player

    @log
    def find_all(self) -> list[Player]:
        """List all players in the database.

        Returns
        -------
        list[Player] sorted by username.
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM player                           "
                        " ORDER BY username;                     "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        players_list = []

        if res:
            for row in res:
                player = Player(
                    id_player=row["id_player"],
                    username=row["username"],
                    password=row["password"],
                    elo=row["elo"],
                    email=row["email"],
                    pokemon_fan=row["pokemon_fan"],
                )

                players_list.append(player)

        return players_list

    @log
    def update(self, player) -> bool:
        """Update a player in the database.

        Parameters
        ----------
        Player to be updated.

        Returns
        -------
        True if update is successful, False otherwise.
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE player                                       "
                        "   SET username = %(username)s,                     "
                        "       password = COALESCE(%(password)s, password), "
                        "       elo = %(elo)s,                               "
                        "       email = %(email)s,                           "
                        "       pokemon_fan = %(pokemon_fan)s                "
                        " WHERE id_player = %(id_player)s;                   ",
                        {
                            "username": player.username,
                            "password": player.password,
                            "elo": player.elo,
                            "email": player.email,
                            "pokemon_fan": player.pokemon_fan,
                            "id_player": player.id_player,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def delete(self, player) -> bool:
        """Delete a player from the database

        Parameters
        ----------
        Player to delete from the database

        Returns
        -------
        True if the player was successfully deleted, False otherwise.
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM player                               "
                        " WHERE id_player = %(id_player)s                 ",
                        {"id_player": player.id_player},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def login(self, username, password) -> Player:
        """Login using username and password

        Parameters
        ----------
        username : str
        password : str

        Returns
        -------
        Player or None
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM player                          "
                        " WHERE username = %(username)s         "
                        "   AND password = %(password)s;        ",
                        {"username": username, "password": password},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        player = None

        if res:
            player = Player(
                username=res["username"],
                password=res["password"],
                elo=res["elo"],
                email=res["email"],
                pokemon_fan=res["pokemon_fan"],
                id_player=res["id_player"],
            )

        return player
