class Player:
    """
    Class representing a Player

    Attributes
    ----------
    id_player : int
        identifier
    username : str
        player's username
    password : str
        player's password
    elo : int
        player's elo rating
    email : str
        player's email
    pokemon_fan : bool
        indicates whether the player is a Pokémon fan
    """

    def __init__(self, username, elo, email, password=None, pokemon_fan=False, id_player=None):
        """Constructor"""
        self.id_player = id_player
        self.username = username
        self.password = password
        self.elo = elo
        self.email = email
        self.pokemon_fan = pokemon_fan

    def __str__(self):
        """Returns a string representation of the player"""
        return f"Player({self.username}, elo: {self.elo})"

    def as_list(self) -> list[str]:
        """Returns the player's attributes as a list"""
        return [self.username, self.elo, self.email, self.pokemon_fan]
