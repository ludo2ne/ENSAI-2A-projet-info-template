# controller/player_controller.py

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.player_service import PlayerService

router = APIRouter()
player_service = PlayerService()


class PlayerModel(BaseModel):
    """Define a Pydantic model for Players"""

    id_player: int | None = None
    username: str
    password: str
    elo: int
    email: str
    pokemon_fan: bool


@router.get("/", tags=["Players"])
async def find_all_players():
    """List all players"""
    logging.info("List all players")
    players_list = player_service.find_all()
    return players_list


@router.get("/{id_player}", tags=["Players"])
async def player_by_id(id_player: int):
    """Find a player by id"""
    logging.info("Find a player by id")
    player = player_service.find_by_id(id_player)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.post("/", tags=["Players"])
async def create_player(p: PlayerModel):
    """Create a player"""
    logging.info("Create a player")
    if player_service.username_already_used(p.username):
        raise HTTPException(status_code=400, detail="Username already used")

    player = player_service.create(p.username, p.password, p.elo, p.email, p.pokemon_fan)
    if not player:
        raise HTTPException(status_code=500, detail="Error while creating player")

    return player


@router.put("/{id_player}", tags=["Players"])
async def update_player(id_player: int, p: PlayerModel):
    """Update a player"""
    logging.info("Update a player")
    player = player_service.find_by_id(id_player)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.username = p.username
    player.password = p.password
    player.elo = p.elo
    player.email = p.email
    player.pokemon_fan = p.pokemon_fan

    player = player_service.update(player)
    if not player:
        raise HTTPException(status_code=500, detail="Error while updating player")

    return f"Player {p.username} updated"


@router.delete("/{id_player}", tags=["Players"])
async def delete_player(id_player: int):
    """Delete a player"""
    logging.info("Delete a player")
    player = player_service.find_by_id(id_player)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player_service.delete(player)
    return f"Player {player.username} deleted"
