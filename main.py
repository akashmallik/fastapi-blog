from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'Name': 'FastAPI Blog', 'Version': 'v0.1'}}


@app.get('/about')
def about():
    return {'data': 'about page'}


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
