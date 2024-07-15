from typing import Any, Union
from fastapi import FastAPI

from video_utility.video_model import Video
from video_utility.video_utility import download_video_from_url

app = FastAPI()

video_db: list[Video] = []
       
       
# TODO 1. Install Python dependencies (pydantic, yt-dlp)
# TODO 2. Try out yt-dlp 
# TODO 3. Add proper starting page
# TODO 4. Download YT video via REST PUT call
# TODO 5. list all existing videos via REST call

# TODO add all exising videos to video_db


@app.get("/")
async def read_root() -> dict[str, str]:
    # TODO return proper starting page
    return {"Hello": "Planet"}

@app.get("/list")
async def get_video_list() -> list[Video]:
    # TODO convert list to dictionary
    return video_db


# Why `put` instead of `post`?
# See: https://restfulapi.net/rest-put-vs-post/
@app.put('/videos/download_video')
async def download_video(video: Video) -> Video:
    """Downloads the video onto the server for later retrieval

    Parameters
    ----------
    

    Returns
    -------
    JSON
        Returns a description of the success and infos of the downloaded video
    """
    # TODO validate URL (for later)
    # TODO download video using yt-dlp
    # TODO return meaningful response, handle errors too!
    
    # download_video_from_url(...)
    return video
