from pydantic import BaseModel


class URL(BaseModel):
    """TODO Add description

    Parameters
    ----------
    BaseModel : URL
        TODO
    """
    url: str


class Video(BaseModel):
    """TODO Add description

    Parameters
    ----------
    BaseModel : Video
        TODO
    """

    name: str
    path: str
