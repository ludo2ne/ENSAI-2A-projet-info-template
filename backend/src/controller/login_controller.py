import logging

from fastapi import APIRouter, HTTPException

from schema.player_model import PlayerLoginModel
from service.player_service import PlayerService

router = APIRouter()
service = PlayerService()


@router.post("/", tags=["Login"])
def login(req: PlayerLoginModel):
    logging.info("Login")
    player = service.login(req.username, req.password)
    if player:
        return {"id_player": player.id_player, "username": player.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")
