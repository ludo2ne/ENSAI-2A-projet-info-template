from business_object.player import Player
from dao.player_dao import PlayerDao
from utils.log_decorator import log
from utils.security import hash_password


class PlayerService:
    """Service that handles business logic related to players (creation, search, etc.)."""

    @log
    def create(self, username, password, elo, email, pokemon_fan) -> Player:
        """Creates a new player in the system.
        Parameters
        ----------
        username : str
        password : str (will be hashed before storage).
        elo : int
        email : str
        pokemon_fan : bool

        Returns
        -------
        Player object created or None if creation failed."""

        new_player = Player(
            username=username,
            password=hash_password(password, username),
            elo=elo,
            email=email,
            pokemon_fan=pokemon_fan,
        )

        return new_player if PlayerDao().create(new_player) else None

    @log
    def find_all(self, hide_password=True) -> list[Player]:
        """Retrieves all players from the database.
        Parameters
        ----------
        hide_password : bool
            If False (Defaults), passwords will be set to None for security.

        Returns
        -------
        list[Player]"""
        players = PlayerDao().find_all()
        # TODO
        return players

    @log
    def find_by_id(self, id_player, hide_password=True) -> Player:
        """Finds a specific player by their unique id.
        Parameters
        ----------
        id_player : int

        Returns
        -------
        Player object if found, otherwise None."""
        player = PlayerDao().find_by_id(id_player)
        if hide_password:
            player.password = None
        return player

    @log
    def update(self, player) -> Player:
        """Updates an existing player's information.
        Parameters
        ----------
        Player object containing updated information.

        Returns
        -------
        The updated Player object, or None if the update failed."""
        player.password = hash_password(player.password, player.username)
        return player if PlayerDao().update(player) else None

    @log
    def delete(self, player) -> bool:
        """Delete a player account.
        Parameters
        ----------
        Player object to be deleted.

        Returns
        -------
        True if deletion was successful, False otherwise."""
        return PlayerDao().delete(player)

    @log
    def login(self, username, password) -> Player:
        """Authenticates a player using their credentials.
        Parameters
        ----------
        username : str
        password : str

        Returns
        -------
        Player object if authentication is successful, otherwise None."""
        return PlayerDao().login(username, hash_password(password, username))

    @log
    def username_already_used(self, username) -> bool:
        """Check if a username is already used.
        Parameters
        ----------
        username : str

        Returns
        -------
        True if the username already exists in the database."""
        players = PlayerDao().find_all()
        return username in [p.username for p in players]
