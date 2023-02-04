from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, get_db
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='Social Media API',
                                user='postgres', password='xaea-1212', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

myPosts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "favorite foods", "content": "I like pizzas", "id": 2}]


def find_post(id):
    for p in myPosts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(myPosts):
        if p['id'] == id:
            return i


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hare Krishna"}
