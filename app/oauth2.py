from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext

from .schemas import TokenData

from jwt.exceptions import InvalidTokenError

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .database import get_db
from .models import User as User_Model
from .config import settings



SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire_time

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token:str, credentials_exception:HTTPException):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get('user_id')

        if not id:
            raise credentials_exception

        token_data = TokenData(id=id)

    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not find valid credentials ", headers={"www-Authenticate":'Bearer'})
    user_id = verify_access_token(token, credentials_exception)

    user = db.query(User_Model).filter(User_Model.id == user_id.id).first()

    return user