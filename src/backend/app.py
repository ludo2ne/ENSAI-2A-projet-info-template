# app.py

import logging

import dotenv
from controller import connexion_controller, joueur_controller
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from utils.log_init import initialiser_logs

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


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
    logging.info("Arrêt du Webservice")
