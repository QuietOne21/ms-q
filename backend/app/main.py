from fastapi import FastAPI

from app.database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "connected"}


