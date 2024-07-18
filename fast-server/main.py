from pathlib import Path
import logging
import os
import subprocess

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from video_utility.model import URL, Video

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.mount('/static', StaticFiles(directory='static'), name='static')


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


video_db: list[Video] = []

for video_file in os.listdir('downloads/'):
    if video_file.endswith('.mp4') or video_file.endswith('.webm'):
        video = Video(name=video_file, path=os.path.join(
            'downloads', video_file))
        video_db.append(video)


@app.get("/")
async def read_root() -> HTMLResponse:
    return HTMLResponse(content=INDEX_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@ app.get("/add")
async def add_video() -> HTMLResponse:
    return HTMLResponse(content=ADD_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@app.get("/download")
async def download_video() -> HTMLResponse:
    return HTMLResponse(content=DOWNLOAD_HTML_FILE_CONTENT, status_code=status.HTTP_201_CREATED)


@app.put("/download")
async def download_video_via_url(url_model: URL) -> HTMLResponse:
    try:

        background_command = [
            'yt-dlp',
            '-o', os.path.join(OUTPUT_PATH, '%(title)s.%(ext)s'),
            url_model.url,
        ]
        subprocess.run(background_command, check=True)

        return HTMLResponse(content=f"Video {url_model.url} downloaded successfully", status_code=status.HTTP_201_CREATED)

    except subprocess.CalledProcessError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@ app.get('/list')
async def video_list() -> HTMLResponse:
    return HTMLResponse(content=LIST_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@app.post("/submit")
async def submit(request: Request) -> HTMLResponse:
    data = await request.json()
    text_value = data.get("text")
    print(f"Received text: {text_value}")

    return HTMLResponse(
        content={"message": "Text received", "text": text_value},
        status_code=status.HTTP_201_CREATED
    )
