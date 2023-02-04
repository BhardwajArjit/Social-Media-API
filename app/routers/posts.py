from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional, List
from .. import oauth

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def getPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth.getCurrentUser)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db),
               current_user: int = Depends(oauth.getCurrentUser)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(1, 1000000)
    # myPosts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def getPost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.getCurrentUser)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.getCurrentUser)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    # myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def updatePost(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
               current_user: int = Depends(oauth.getCurrentUser)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # myPosts[index] = post_dict
    return post_query.first()
