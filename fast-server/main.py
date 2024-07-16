from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from urllib.parse import urlparse
import logging
import os
import subprocess


from video_utility.model import URL, Video

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

OUTPUT_PATH: str = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

video_db: list[Video] = []


def url_check(url):
    try:
        result = urlparse(url)

        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False


# TODO 1. Install Python dependencies (pydantic, yt-dlp) [done]
# TODO 2. Try out yt-dlp [done]
# TODO 3. Add proper starting page [done]
# TODO 4. Download YT video via REST PUT call [done]
# TODO 5. download.html for REST GET request
# TODO 6. add all exising videos to video_db
# TODO 7. list all existing videos via REST call


@app.put("/download")
async def download_video_via_url(video: URL):
    # TODO add code to run yt-dlp "url" so the video will be downloadet automatically
    # TODO fix error 405
    try:

        background_command = [
            'yt-dlp',
            '-o', os.path.join(OUTPUT_PATH, '%(title)s.%(ext)s'),
            video.url,
        ]
        subprocess.run(background_command, check=True)

        return {"message": "Video downloaded successfully", "path": OUTPUT_PATH}

    except subprocess.CalledProcessError as error:
        raise HTTPException(status_code=400, detail=str(error))
    

@app.get("/download")
async def download_video():
    try:

        index_file_path = Path("download.html")

        if index_file_path.exists():
            content = index_file_path.read_text(encoding='utf-8')
            # logging.debug(f"File content: {content}")
            return HTMLResponse(content=content, status_code=200)
            # logging.debug(f"Index file found at {index_file_path}")
            # return HTMLResponse(content=index_file_path.read_text(), status_code=200)
        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")

    except Exception as e:
        logging.exception(
            f"An error occurred while reading the index file {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
async def read_root() -> dict[str, str]:
    # TODO return proper starting page [done]
    try:

        index_file_path = Path("index.html")

        if index_file_path.exists():
            content = index_file_path.read_text(encoding='utf-8')
            # logging.debug(f"File content: {content}")
            return HTMLResponse(content=content, status_code=200)
            # logging.debug(f"Index file found at {index_file_path}")
            # return HTMLResponse(content=index_file_path.read_text(), status_code=200)
        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")

    except Exception as e:
        logging.exception(
            f"An error occurred while reading the index file {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#    index_file_path = Path("/mnt/c/Users/Luka/IdeaProjects/untitled1/media-server-client/fast-server/index.html")
#    if index_file_path.exists():
#        return HTMLResponse(content=index_file_path.read_text(), status_code=200)


@app.get("/list")
async def get_video_list() -> list[Video]:
    # TODO convert list to dictionary
    return video_db

#@app.get("/list")
#async def download_video():
#    try:
#
#        index_file_path = Path("list.html")
#
#        if index_file_path.exists():
#            content = index_file_path.read_text(encoding='utf-8')
#            # logging.debug(f"File content: {content}")
#            return HTMLResponse(content=content, status_code=200)
#            # logging.debug(f"Index file found at {index_file_path}")
#            # return HTMLResponse(content=index_file_path.read_text(), status_code=200)
#        else:
#            logging.error(f"Index file not found at {index_file_path}")
#            raise HTTPException(status_code=404, detail="Index file not found")
#
#    except Exception as e:
#        logging.exception(
#            f"An error occurred while reading the index file {e}")
#        raise HTTPException(status_code=500, detail="Internal Server Error")





# Why `put` instead of `post`?
# See: https://restfulapi.net/rest-put-vs-post/
# @app.put('/videos/download_video')
# async def download_video(video: Video) -> Video:
#    """Downloads the video onto the server for later retrieval
#
#    Parameters
#    ----------
#
#
#    Returns
#    -------
#    JSON
#        Returns a description of the success and infos of the downloaded video
#    """
#    # TODO validate URL (for later) [done]
#    # TODO download video using yt-dlp
#    # TODO return meaningful response, handle errors too!
#
#    # download_video_from_url(...)
#    return video
