from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from .. import schemas, database, models

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)


@router.get('/', response_model=List[schemas.ShowBlog])
def index(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")

    blog.update(request)
    db.commit()

    return 'updated'


@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available...."}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")

    return blog


@router.delete('/{id}')
def delete(id: int, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available...."}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")
    
    blog.delete()
    db.commit()

    return 'Deleted!'
