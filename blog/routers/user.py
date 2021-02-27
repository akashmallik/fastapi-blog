from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .. import schemas, database
from .. import models
from ..hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post('/', response_model=schemas.ShowUser)
def user(request: schemas.User, db: Session = Depends(database.get_db)):
    user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get('/{id}', response_model=schemas.ShowUser)
def show_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not available.")
    
    return user
