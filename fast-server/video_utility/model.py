from pydantic import BaseModel


class URL(BaseModel):
    url: str


class Video(BaseModel):

    name: str
    path: str
