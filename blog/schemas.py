from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    title: str
    body: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    creator: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
