from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase): # Here we design what data to send exactly in response
    id : int
    created_at : datetime
    class Config:
        from_attributes = True