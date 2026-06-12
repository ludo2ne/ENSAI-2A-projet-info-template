from pydantic import BaseModel


class GameModel(BaseModel):
    id_opponent: int
    choice: str
