from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    # rating: Optional[int] = None


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


@app.get("/")
async def root():
    return {"message": "Hare Krishna"}


@app.get("/posts")
def getPosts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(1, 1000000)
    # myPosts.append(post_dict)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def getPost(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.publish, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # myPosts[index] = post_dict
    return {'data': updated_post}
