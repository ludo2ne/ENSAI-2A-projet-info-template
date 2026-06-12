from pydantic import BaseModel


class GameModel(BaseModel):
    id_player1: int
    id_player2: int
    choice: str
