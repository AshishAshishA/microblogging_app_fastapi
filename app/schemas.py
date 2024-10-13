from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional

class BasePost(BaseModel):
    title:str
    content:str
    published:bool = True

class CreatePost(BasePost):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime.datetime

class Post(BasePost):
    id:int
    created_at:datetime.datetime
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode = True

class User(BaseModel):
    email:EmailStr
    password:str




class UserLogin(User):
    pass

class Token(BaseModel):
    token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]

class Votes(BaseModel):
    post_id:int
    dir:int
