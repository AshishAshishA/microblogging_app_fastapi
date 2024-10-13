from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional,List
import psycopg2
from psycopg2.extras import RealDictCursor

from .models import Post as Post_Model, User as User_Model
from .database import Base,engine,  get_db
from sqlalchemy.orm import Session, query

from .schemas import CreatePost, Post, User, UserOut

from .utils import hash;

from .router import posts, users, login, votes

from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

myapp2 = FastAPI()

# origins = [
#     "https://www.google.com/",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

myapp2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@myapp2.get('/', status_code=status.HTTP_200_OK)
def root():
    return {"message":"app is working...."}

myapp2.include_router(posts.router)
myapp2.include_router(users.router)
myapp2.include_router(login.router)
myapp2.include_router(votes.router)