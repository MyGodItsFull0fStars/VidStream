import logging
import os
import subprocess
import time
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.templating import _TemplateResponse
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")


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
VIDEO_DIR = 'downloads'
# PROGRESS_FILE = "progress.txt"

# for video_file in os.listdir('downloads/'):
#     if video_file.endswith('.mp4') or video_file.endswith('.webm'):
#         video = Video(name=video_file, path=os.path.join('downloads', video_file))
#         video_db.append(video)

# def download_simulation(file_name: str):
#     global PROGRESS
#     total_steps = 10
#     for step in range(total_steps):
#         PROGRESS = (step + 1) / total_steps * 100
#         time.sleep(1)  # Simulate time taken for downloading each chunk
#     # Simulate moving the file to the video directory
#     os.makedirs(VIDEO_DIR, exist_ok=True)
#     shutil.copy(file_name, os.path.join(VIDEO_DIR, os.path.basename(file_name)))
#     PROGRESS = 100
for video_file in os.listdir('downloads/'):
    if video_file.endswith('.mp4') or video_file.endswith('.webm'):
        video = Video(name=video_file, path=os.path.join(
            'downloads', video_file))
        video_db.append(video)


@app.get("/")
async def read_root() -> HTMLResponse:
    return HTMLResponse(content=INDEX_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@app.get("/items/", response_class=HTMLResponse)
async def read_item(request: Request):
    # id = 'test'
    return templates.TemplateResponse(
        request=request, name="aaa.html", context={"id": len(video_db)}
    )


@app.get("/videos/list", response_class=HTMLResponse)
async def list_videos_template(request: Request) -> _TemplateResponse:

    return templates.TemplateResponse(
        request=request, name="video_list.html", context={"videos": video_db}
    )


@app.get("/videos/{video_name}")
async def get_video(video_name: str):
    video_path = os.path.join(VIDEO_DIR, video_name)
    return FileResponse(video_path)


@app.get('/list/a')
async def list_videos():
    videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".webm", ".ogg"))]
    v_name = [f.split('.')[0] for f in videos]
    return [
        Video(name=v_name[i], path=videos[i]) for i in range(len(videos))
    ]
    #return {"videos": videos}, HTMLResponse (content=LIST_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)
    videos = [f for f in os.listdir(
        VIDEO_DIR) if f.endswith((".mp4", ".webm", ".ogg"))]
    return {"videos": videos}, HTMLResponse(content=LIST_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@ app.get('/list')
async def video_list() -> HTMLResponse:
    return HTMLResponse(content=LIST_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
        raise HTTPException(status_code=400, detail=str(error))

# @app.post("/download")
# async def start_download(background_tasks: BackgroundTasks):
#     background_tasks.add_task(download_simulation, "dummy_video.mp4")
#     return {"message": "Download started"}

# @app.get("/progress")
# async def get_progress():
#     if os.path.exists(PROGRESS_FILE):
#         with open(PROGRESS_FILE, 'r') as f:
#             lines = f.readlines()
#             if lines:
#                 return {"progress": float(lines[-1])}
#     return {"progress": 0}


# @app.post("/download")
# async def start_download(background_tasks: BackgroundTasks):
#     global PROGRESS
#     PROGRESS = 0
#     background_tasks.add_task(download_simulation, "dummy_video.mp4")
#     return {"message": "Download started"}

# @app.get("/progress")
# async def get_progress():
#     return {"progress": PROGRESS}
    
        

        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


# @ app.get('/list')
# async def video_list() -> HTMLResponse:
#     return HTMLResponse(content=LIST_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@app.post("/submit")
async def submit(request: Request) -> HTMLResponse:
    data = await request.json()
    text_value = data.get("text")
    print(f"Received text: {text_value}")

    return HTMLResponse(
        content={"message": "Text received", "text": text_value},
        status_code=status.HTTP_201_CREATED
    )
