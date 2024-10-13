from fastapi import status, HTTPException, APIRouter, Depends
from ..schemas import User, UserOut
from ..utils import hash
from ..models import User as User_Model
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session, query

router = APIRouter(
    tags=['users'],
    prefix="/users"
)


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:User, db:Session = Depends(get_db)):

    hashed_passwd = hash(user.password)
    user.password = hashed_passwd

    new_user = User_Model(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db:Session=Depends(get_db), curr_user = Depends(get_current_user)):
    print(curr_user.email)
    user = db.query(User_Model).filter(User_Model.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found")
    
    return user