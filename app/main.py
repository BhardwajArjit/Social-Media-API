from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


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


@app.get("/")
async def root():
    return {"message": "Hare Krishna"}


@app.get("/posts")
def getPosts():
    return {"data": myPosts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 1000000)
    myPosts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def getPost(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    myPosts[index] = post_dict
    return {'data': post_dict}
