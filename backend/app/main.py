from fastapi import FastAPI

from app.database import engine
from sqlalchemy import text

from app.database import engine, Base
from app.models import user, restaurant, restaurant_table, menu_category, menu_item, reservation

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "connected"}


