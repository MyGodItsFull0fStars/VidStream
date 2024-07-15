from typing import Any, Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import logging


from video_utility.video_model import Video
from video_utility.video_utility import download_video_from_url

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

video_db: list[Video] = []
       
       
# TODO 1. Install Python dependencies (pydantic, yt-dlp) [done]
# TODO 2. Try out yt-dlp [done]
# TODO 3. Add proper starting page [done]
# TODO 4. Download YT video via REST PUT call
# TODO 5. list all existing videos via REST call

# TODO add all exising videos to video_db


@app.get("/")
async def read_root() -> dict[str, str]:
    # TODO return proper starting page [done]
    try:
        index_file_path = Path("/mnt/c/Users/Luka/IdeaProjects/untitled1/media-server-client/fast-server/index.html")
        if index_file_path.exists():
            content = index_file_path.read_text()
            logging.debug(f"File content: {content}")
            return HTMLResponse(content=content, status_code=200)
            #logging.debug(f"Index file found at {index_file_path}")
            #return HTMLResponse(content=index_file_path.read_text(), status_code=200)
        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")
    except Exception as e:
        logging.exception("An error occurred while reading the index file")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#    index_file_path = Path("/mnt/c/Users/Luka/IdeaProjects/untitled1/media-server-client/fast-server/index.html")
#    if index_file_path.exists():
#        return HTMLResponse(content=index_file_path.read_text(), status_code=200)

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
