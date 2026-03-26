# app.py

import logging

import dotenv
from controller import connexion_controller, joueur_controller
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from utils.log_init import initialiser_logs
from utils.reset_database import ResetDatabase

# Initialisation
initialiser_logs("Webservice")
dotenv.load_dotenv()

app = FastAPI(title="Mon webservice")

app.include_router(joueur_controller.router, prefix="/joueur", tags=["Joueurs"])
app.include_router(connexion_controller.router, prefix="/connexion", tags=["Connexion"])


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/hello/{name}", tags=["Divers"])
async def hello_name(name: str):
    """Afficher Hello"""
    logging.info("Afficher Hello")
    return {"message": f"Hello {name}"}


@app.get("/reset_database", tags=["Divers"])
async def reset_database():
    """Réinitialiser la base de données"""
    logging.info("Réinitialisation de la base de données")
    succes = ResetDatabase().lancer()

    return {
        "message": f"Ré-initilisation de la base de données - {'SUCCES' if succes else 'ECHEC'}"
    }


# Run the FastAPI application
if __name__ == "__main__":
    import os

    import dotenv
    import uvicorn

    dotenv.load_dotenv(override=True)

    uvicorn.run(
        app,
        host=os.getenv("UVICORN_HOST", "127.0.0.1"),
        port=int(os.getenv("UVICORN_PORT", "5000")),
    )

    logging.info("Arret du Webservice")
