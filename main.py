from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None

my_posts=[
    {
        "title" : "my BMW car",
        "content" : " red color",
        "id" : 1
    },
    {
        "title" : "my Toyota car",
        "content" : "white color",
        "id" : 2
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 500)
    my_posts.append(post_dict)
    return {"new_post" : post_dict}


@app.get("/posts/{id}")
async def get_posts(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"data" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id : int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_posts(id: int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}