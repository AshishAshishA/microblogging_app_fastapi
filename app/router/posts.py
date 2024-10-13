from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..schemas import CreatePost, Post, User, PostOut
from ..utils import hash
from ..models import Post as Post_Model, Vote as Vote_Model
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session, query
from sqlalchemy import func
from ..oauth2 import get_current_user

router = APIRouter(
    tags=['posts'],
    prefix="/posts"
)

@router.get('/',status_code=status.HTTP_200_OK, response_model=List[PostOut])
def get_posts(db:Session = Depends(get_db), curr_user:User = Depends(get_current_user), limit:int = 10, skip:int = 0, search:Optional[str]=""):
    # print(curr_user.email)
    
    
    join_query = db.query(Post_Model, func.count(Vote_Model.post_id).label("votes")).join(Vote_Model, Post_Model.id==Vote_Model.post_id, isouter=True).group_by(Post_Model.id)
    filter_query = join_query.filter(Post_Model.title.icontains(search)).limit(limit).offset(skip)
    
    posts = filter_query.all()
    
    return posts

@router.get('/{id}', response_model=PostOut)
def get_post(id:int,db:Session = Depends(get_db), curr_user:int = Depends(get_current_user)):

    join_query = db.query(Post_Model, func.count(Vote_Model.post_id).label("votes")).join(Vote_Model, Post_Model.id==Vote_Model.post_id, isouter=True).group_by(Post_Model.id)
    post = join_query.filter(Post_Model.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    
    return post

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post:CreatePost, db :Session=Depends(get_db), response_model=Post, curr_user:int = Depends(get_current_user)):
  
    new_post = Post_Model(owner_id = curr_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}')
def delete_post(id:int, db:Session = Depends(get_db), curr_user:int = Depends(get_current_user)):

    post_query = db.query(Post_Model).filter(Post_Model.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found")

    if post.owner_id != curr_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"owner doesn't match")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message':f'post with id: {id} deleted'}

@router.put('/{id}', response_model=Post)
def update_post(id:int, post:CreatePost, db:Session=Depends(get_db), curr_user:int = Depends(get_current_user)):
  
    update_post_query = db.query(Post_Model).filter(Post_Model.id == id)

    to_update_post = update_post_query.first()
    
    if not to_update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    if to_update_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"owner doesn't match") 
    
    update_post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return update_post_query.first()