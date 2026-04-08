from business_object.player import Player
from dao.player_dao import PlayerDao
from utils.log_decorator import log
from utils.security import hash_password


class PlayerService:
    """Class containing Player service methods"""

    @log
    def create(self, username, password, elo, email, pokemon_fan) -> Player:
        """Create a player from given attributes"""

        new_player = Player(
            username=username,
            password=hash_password(password, username),
            elo=elo,
            email=email,
            pokemon_fan=pokemon_fan,
        )

        return new_player if PlayerDao().create(new_player) else None

    @log
    def find_all(self, include_password=False) -> list[Player]:
        """List all players
        If include_password=True, passwords will be included
        By default, all player passwords are set to None
        """
        players = PlayerDao().find_all()
        if not include_password:
            for p in players:
                p.password = None
        return players

    @log
    def find_by_id(self, id_player) -> Player:
        """Find a player by their id"""
        return PlayerDao().find_by_id(id_player)

    @log
    def update(self, player) -> Player:
        """Update a player"""

        player.password = hash_password(player.password, player.username)
        return player if PlayerDao().update(player) else None

    @log
    def delete(self, player) -> bool:
        """Delete a player account"""
        return PlayerDao().delete(player)

    @log
    def login(self, username, password) -> Player:
        """Login using username and password"""
        return PlayerDao().login(username, hash_password(password, username))

    @log
    def username_already_used(self, username) -> bool:
        """Check if a username is already used
        Returns True if the username already exists in the database
        """
        players = PlayerDao().find_all()
        return username in [p.username for p in players]
