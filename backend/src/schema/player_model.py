from pydantic import BaseModel, EmailStr, Field


class PlayerCreateUpdateModel(BaseModel):
    """Acts as the data contract between the frontend and the backend.

    It defines the JSON structure used to exchange player information,
    ensuring data consistency and validation during API requests and responses."""

    id_player: int | None = None
    username: str
    password: str = Field(..., min_length=35)
    elo: int
    email: EmailStr
    pokemon_fan: bool


class PlayerReadModel(BaseModel):
    id_player: int
    username: str
    elo: int | None
    email: EmailStr
    pokemon_fan: bool | None


class PlayerLoginModel(BaseModel):
    username: str
    password: str
