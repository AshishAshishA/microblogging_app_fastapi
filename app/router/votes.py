from fastapi import status, HTTPException, APIRouter, Depends
from ..schemas import Votes
from ..models import Vote as Vote_Model, Post as Post_Model
from ..database import get_db
from sqlalchemy.orm import Session, query
from ..oauth2 import get_current_user

router = APIRouter(
    tags=['votes'],
    prefix="/votes"
)

@router.post('/')
def votes(vote:Votes, db:Session = Depends(get_db), curr_user = Depends(get_current_user)):
    post = db.query(Post_Model).filter(Post_Model.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does not found')

    vote_query = db.query(Vote_Model).filter(Vote_Model.post_id == vote.post_id, Vote_Model.user_id==curr_user.id)

    if vote.dir == 1:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'vote for post with id {vote.post_id} already exist')
        new_vote = Vote_Model(post_id = vote.post_id, user_id = curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"vote is successfully added"}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote doesn\'t exist')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"vote is succesfully deleted"}

