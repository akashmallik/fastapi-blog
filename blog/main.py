from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from typing import List


from . import models, schemas
from .database import engine, SessionLocal
from .hashing import Hash


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def index(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")

    blog.update(request)
    db.commit()

    return 'updated'


@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available...."}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")

    return blog


@app.delete('/blog/{id}', tags=['blogs'])
def delete(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available...."}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")
    
    blog.delete()
    db.commit()

    return 'Deleted!'


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def user(request: schemas.User, db: Session = Depends(get_db)):
    user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not available.")
    
    return user
