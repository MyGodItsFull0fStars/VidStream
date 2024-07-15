from uuid import uuid4
from pydantic import BaseModel


class Video(BaseModel):
    # id = str(uuid4())
    url: str
    # name: str | None = None
    # description: str | None = None
    # video_file_path: str | None

    def from_file(video_file_path: str) -> "Video":
        # TODO load video instance from given file path

        return Video(name='test', url='not saved')
