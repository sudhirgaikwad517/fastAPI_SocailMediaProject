from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None
    
try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='root',cursor_factory=RealDictCursor)
    cur = conn.cursor()
    print("Database connected successfully")
except Exception as error:
    print("The error while connecting :",error)

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"favorite foods","content":"I like pizza","id":2}]

@app.get("/")
async def root():
    return {"Message":"Hello World"}

@app.get("/posts")
def posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"Data":posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def createpost(post : Post):
    cur.execute("""INSERT INTO posts (title , content , published) VALUES (%s,%s,%s) RETURNING *""" , (post.title , post.content , post.published))
    new_post = cur.fetchall()
    conn.commit()
    return {"Post" : new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cur.fetchone()
    if post:
            return {"Post_detail":post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")

@app.delete("/posts/{id}")
def delete_post(id: int):
    cur.execute("""DELETE from posts WHERE id = %s returning *""" , (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()

    if deleted_post == None :
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")
    return {"Message" : "Post Deleted Successfuly", "Data" : deleted_post}        
@app.put("/posts/{id}")    
def update_post(id: int, post: Post):
    cur.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")
    return updated_post