#cd backend
# uvicorn src.main:app --reload --host 0.0.0.0 --port 5000

# PYTHONPATH=backend/src uvicorn backend.src.main:app --reload --env-file backend/.env

python backend/src/main.py