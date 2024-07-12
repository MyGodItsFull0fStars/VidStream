from typing import Any, Union
from fastapi import FastAPI

from video_utility.video_model import Video

app = FastAPI()

video_db: list[Video] = []

# TODO add all exising videos to video_db


@app.get("/")
async def read_root() -> dict[str, str]:
    # TODO return proper starting page
    return {"Hello": "World"}


# Why `put` instead of `post`?
# See: https://restfulapi.net/rest-put-vs-post/
@app.put('/videos/download_video')
async def download_video(video: Video) -> Video:
    """Downloads the video onto the server for later retrieval

    Parameters
    ----------
    url : str
        the source URL of the video

    Returns
    -------
    JSON
        Returns a description of the success and infos of the downloaded video
    """
    # TODO validate URL
    # TODO download video using yt-dlp
    # TODO return meaningful response, handle errors too!
    return video
