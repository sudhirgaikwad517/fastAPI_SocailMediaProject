from fastapi import FastAPI , Response , status , HTTPException , Depends
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas
from .database import engine ,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
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

@app.get("/posts",response_model=List[schemas.Post])
def posts(db:Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",response_model=schemas.Post,status_code = status.HTTP_201_CREATED)
def createpost(post : schemas.PostBase , db:Session = Depends(get_db)):
    # cur.execute("""INSERT INTO posts (title , content , published) VALUES (%s,%s,%s) RETURNING *""" , (post.title , post.content , post.published))
    # new_post = cur.fetchall()
    # conn.commit()
    # new_post = models.Post(title = post.title , content = post.content , published = post.published)
    post_data = post.dict(exclude_unset=True)
    new_post = models.Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def get_post(id: int,db:Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
            return {"Post_detail":post}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")

@app.delete("/posts/{id}")
def delete_post(id: int,db:Session = Depends(get_db)):
    # cur.execute("""DELETE from posts WHERE id = %s returning *""" , (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None :
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"Message" : "Post Deleted Successfuly"}        
@app.put("/posts/{id}")    
def update_post(id: int, updated_post: schemas.PostBase,db:Session = Depends(get_db)):
    # cur.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} was not found")
    update_data = updated_post.dict(exclude={'rating'})
    post_query.update( update_data,synchronize_session=False) #type: ignore
    db.commit()
    return {"Updated" : post_query.first()}