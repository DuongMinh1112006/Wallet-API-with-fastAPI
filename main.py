from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional[int] = None

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.post("/users/")
async def read_user(post: Post):
    print(post.rating)
    print(post.dict())
    return {"new_post" : post}