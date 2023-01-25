from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hare Krishna"}


@app.get("/posts")
def getPosts():
    return {"data": "This is your post"}


@app.post("/createposts")
def createPost(post: Post):
    print(post.dict())
    return {"data": post}
