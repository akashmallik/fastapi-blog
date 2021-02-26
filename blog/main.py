from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from . import models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/blog')
def index(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(
        title=request.title,
        body=request.body
    )

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


@app.get('/blog/{id}')
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available...."}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available.")

    return blog
