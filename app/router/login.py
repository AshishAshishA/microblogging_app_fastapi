
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..schemas import UserLogin, Token
from ..models import User as User_Model
from ..utils import verify
from ..database import get_db
from sqlalchemy.orm import Session, query
from ..oauth2 import create_access_token

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=Token)
def login(user:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user_db = db.query(User_Model).filter(User_Model.email == user.username).first()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials are invalid')
    
    if not verify(user.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials are invalid')

    access_token = create_access_token({"user_id":user_db.id})

    token_obj = Token(token=access_token, token_type='Bearer')

    return token_obj