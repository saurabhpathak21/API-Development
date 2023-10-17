from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

my_posts = [
    {
        "title": "Top cities",
        "content": "Checkout the Indian Cities",
        "publish": False,
        "rating": 1,
        "id": 1
    },
    {
        "title": "Top Food",
        "content": "Checkout the Indian Cuisine",
        "publish": False,
        "rating": 4,
        "id": 2
    }
]

def find_post(post_id):
    for p in my_posts:
        if p['id'] == post_id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/v1/")
def get():
    return {"message": "Hello World"}

@app.get("/v1/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/v1/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"message": "Post created successfully"}

@app.get("/v1/posts/latest")
def get_latest_post():
    if my_posts:
        latest_post = my_posts[-1]
        return {"detail": latest_post}
    else:
        return {"detail": "No posts available"}

@app.get("/v1/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    
    return {"post_detail": post}

@app.delete("/v1/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    index = find_index_post(id)
    if index is not None:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")

@app.put("/v1/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is not None:
        my_posts.pop(index)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts.insert(index, post_dict)
    response_data = {
        "message": "Post updated successfully",
        "updated_post": post_dict
    }
    return response_data
