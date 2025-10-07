from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional

app = FastAPI()
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"favorite foods","content":"I like pizza","id":2}]

@app.get("/")
async def root():
    return {"Message":"Hello World"}

@app.get("/posts")
def posts():
    return {"Data":my_posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def createpost(post : Post):
    post_dict  = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"Post" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return {"Post_detail":post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")

@app.delete("/posts/{id}")
def delete_post(id: int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(index)
            return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for index, p in enumerate(my_posts):
        if p['id'] == id:
            my_posts[index] = post.dict()
            my_posts[index]['id'] = id
            return {"data":my_posts[index]}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")