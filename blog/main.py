from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, blog, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)
