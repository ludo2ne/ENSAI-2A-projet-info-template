from pydantic import BaseModel


class GameModel(BaseModel):
    player1_id: int
    player2_id: int
    choice: str
