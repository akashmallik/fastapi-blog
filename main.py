import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


@app.get('/')
def index():
    return {'data': {'Name': 'FastAPI Blog', 'Version': 'v0.1'}}


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.get('/blog')
def blog(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs'}
    else:
        return {'data': f'{limit} blogs'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    # fetch comments of blog with id = id
    return {'data': ['Comments 1', 'comments 2']}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):

    return {'data': f"Blog is created with {blog.title}."}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
