from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.player_service import PlayerService

router = APIRouter()
service = PlayerService()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/", tags=["Login"])
def login(req: LoginRequest):
    player = service.login(req.username, req.password)
    if player:
        return {"id_player": player.id_player, "username": player.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")
