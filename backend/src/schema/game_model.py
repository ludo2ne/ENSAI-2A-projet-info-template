from pydantic import BaseModel


class GamePlayModel(BaseModel):
    id_opponent: int
    choice: str
