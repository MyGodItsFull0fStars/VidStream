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

# TODO add HTML static page paths here
# TODO validate paths (similar to what is already done within REST methods)

OUTPUT_PATH: str = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

assert len(OUTPUT_PATH) > 0, 'invalid output path'

video_db: list[Video] = []

for video in os.listdir('downloads/'):
    if video.endswith('.mp4'):
        video_db.append(video)
    elif video.endswith('.webm'):
        video_db.append(video)


def url_check(url):  # TODO replace with FastAPI/Pydantic validator
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
# TODO 5. download.html for REST GET request [done / also improved index.html]
# TODO 6. add all exising videos to video_db [done]
# TODO 7. list all existing videos via REST call


@app.put("/download")
async def download_video_via_url(url_model: URL) -> HTMLResponse:
    try:

        background_command = [
            'yt-dlp',
            '-o', os.path.join(OUTPUT_PATH, '%(title)s.%(ext)s'),
            url_model.url,
        ]
        subprocess.run(background_command, check=True)

        return HTMLResponse(content=f"Video {url_model.url} downloaded successfully", status_code=201)

    except subprocess.CalledProcessError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/download")
async def download_video() -> HTMLResponse:
    try:

        index_file_path = Path("download.html")  # TODO move up

        if index_file_path.exists():
            content = index_file_path.read_text(encoding='utf-8')
            return HTMLResponse(content=content, status_code=200)
        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")

    except Exception as e:
        logging.exception(
            f"An error occurred while reading the index file {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
async def read_root() -> HTMLResponse:
    try:

        index_file_path = Path("index.html")  # TODO move up

        if index_file_path.exists():
            content = index_file_path.read_text(encoding='utf-8')
            return HTMLResponse(content=content, status_code=200)

        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")

    except Exception as e:
        logging.exception(
            f"An error occurred while reading the index file {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@ app.get('/list')
async def video_list():
    try:
        index_file_path = Path('list.html')  # TODO move up

        if index_file_path.exists():
            content = index_file_path.read_text(encoding='utf-8')
            return HTMLResponse(content=content, status_code=200)
        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")

    except Exception as e:
        logging.exception(
            f"An error occurred while reading the index file {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@ app.get("/listAddManually")
async def add_video_to_list():
    try:

        index_file_path = Path("listAddManually.html")  # TODO move up

        if index_file_path.exists():
            content = index_file_path.read_text(encoding='utf-8')
            return HTMLResponse(content=content, status_code=200)
        else:
            logging.error(f"Index file not found at {index_file_path}")
            raise HTTPException(status_code=404, detail="Index file not found")

    except Exception as e:
        logging.exception(
            f"An error occurred while reading the index file {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
