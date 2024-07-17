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

DOWNLOAD_HTML_FILE_PATH: Path = Path("download.html")
DOWNLOAD_HTML_FILE_CONTENT: Path = DOWNLOAD_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert DOWNLOAD_HTML_FILE_PATH.exists(), 'download.html not found'

OUTPUT_PATH: str = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

assert len(OUTPUT_PATH) > 0, 'invalid output path'

INDEX_HTML_FILE_PATH: Path = Path("index.html")
INDEX_HTML_FILE_CONTENT: Path = INDEX_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert INDEX_HTML_FILE_PATH.exists(), 'index.html not found'

LIST_HTML_FILE_PATH: Path = Path("list.html")
LIST_HTML_FILE_CONTENT: Path = LIST_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert LIST_HTML_FILE_PATH.exists(), 'list.html not found'

ADD_HTML_FILE_PATH: Path = Path("listAddManually.html")
ADD_HTML_FILE_CONTENT: Path = ADD_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert ADD_HTML_FILE_PATH.exists(), 'listAddManually.html not found'

video_db: list[Video] = []  # TODO fill with existing videos


for video in os.listdir('downloads/'):
    if video.endswith('.mp4'):
        video_db.append(video)
    elif video.endswith('.webm'):
        video_db.append(video)


def url_check(url):  
    try:
        result = urlparse(url)

        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False


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
    return HTMLResponse(content=DOWNLOAD_HTML_FILE_CONTENT, status_code=200)


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

        # TODO fill with video_db values
        video_dict: dict[str, str] = {
            # key (name): value (path)
        }

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


@ app.get("/add")
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
