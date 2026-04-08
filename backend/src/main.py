# main.py

import logging

import dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from controller import game_controller, login_controller, player_controller
from utils.log_init import initialize_logs
from utils.reset_database import ResetDatabase

# Initialization
initialize_logs("Webservice")
dotenv.load_dotenv()

app = FastAPI(title="My Webservice")

app.include_router(player_controller.router, prefix="/player", tags=["Players"])
app.include_router(login_controller.router, prefix="/login", tags=["Login"])
app.include_router(game_controller.router, prefix="/game", tags=["Games"])


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/hello/{name}", tags=["Misc"])
async def hello_name(name: str):
    """Display Hello"""
    logging.info("Display Hello")
    return {"message": f"Hello {name}"}


@app.get("/reset_database", tags=["Misc"])
async def reset_database():
    """Reset the database"""
    logging.info("Database reset")
    success = ResetDatabase().run()

    return {"message": f"Database re-initialization - {'SUCCESS' if success else 'FAILURE'}"}


# Run the FastAPI application
if __name__ == "__main__":
    import os

    import dotenv
    import uvicorn

    import utils.env_variables as env_variables

    env_variables.load_environment_variables()
    env_variables.display_values()

    uvicorn.run(
        app,
        host=os.getenv("UVICORN_HOST", "127.0.0.1"),
        port=int(os.getenv("UVICORN_PORT", "5000")),
    )

    logging.info("Webservice stopped")
