from pydantic import BaseModel, field_validator

import re

# Validate URL
url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


class URL(BaseModel):
    """TODO Add description

    Parameters
    ----------
    BaseModel : URL
        TODO
    """
    url: str

    @field_validator('url')
    @classmethod
    def url_validationn(cls, v: str) -> str:
        if v is None or len(v) == 0:
            raise ValueError('empty url')

        if re.match(url_pattern, v) is None:
            raise ValueError('invalid url pattern')

        return v


class Video(BaseModel):
    """TODO Add description

    Parameters
    ----------
    BaseModel : Video
        TODO
    """

    name: str
    path: str


if __name__ == '__main__':
    # if it crashes, there is something with the URL validation
    URL(url='https://www.youtube.com/watch?v=RAjgkqJ-8xQ')
