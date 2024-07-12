from uuid import uuid4
from pydantic import BaseModel


class Video(BaseModel):
    id = str(uuid4())
    name: str
    url: str
    description: str | None = None

    def from_file(video_file_path: str) -> "Video":
        # TODO load video instance from given file path
        pass