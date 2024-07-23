"""This module is the starting point of the `Media-Server` side"""
import logging
import os
import subprocess
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="static/templates")

DOWNLOAD_HTML_FILE_PATH: Path = Path("static/templates/download.html")
DOWNLOAD_HTML_FILE_CONTENT: Path = DOWNLOAD_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert DOWNLOAD_HTML_FILE_PATH.exists(), 'download.html not found'

OUTPUT_PATH: str = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

assert len(OUTPUT_PATH) > 0, 'invalid output path'

INDEX_HTML_FILE_PATH: Path = Path("static/templates/index.html")
INDEX_HTML_FILE_CONTENT: Path = INDEX_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert INDEX_HTML_FILE_PATH.exists(), 'index.html not found'

LIST_HTML_FILE_PATH: Path = Path("static/templates/list.html")
LIST_HTML_FILE_CONTENT: Path = LIST_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert LIST_HTML_FILE_PATH.exists(), 'list.html not found'

ADD_HTML_FILE_PATH: Path = Path("static/templates/listAddManually.html")
ADD_HTML_FILE_CONTENT: Path = ADD_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert ADD_HTML_FILE_PATH.exists(), 'listAddManually.html not found'


VIDEO_DIR = 'downloads'


video_db: list[Video] = []
for video_file in os.listdir('downloads/'):
    if video_file.endswith('.mp4') or video_file.endswith('.webm'):
        video = Video(name=video_file, path=os.path.join(
            'downloads', video_file))
        video_db.append(video)


@app.get("/")
async def read_root() -> HTMLResponse:
    """Homepage

    Returns
    -------
    HTMLResponse
        A HTML Page consisting every important redirect 
    """
    return HTMLResponse(content=INDEX_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)


@app.get("/list", response_class=HTMLResponse)
async def list_videos_template(request: Request) -> HTMLResponse:
    """Returns a HTML page listing all available videos

    Parameters
    ----------
    request : Request
        HTTP request

    Returns
    -------
    HTMLResponse
        A HTML page consisting of available videos
    """
    videos = [{"name": f.split('.')[0], "path": f"/videos/{f}"}
              for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".webm", ".ogg"))]

    return templates.TemplateResponse(
        request=request,
        name="list.html",
        context={"videos": videos},
        status_code=status.HTTP_200_OK
    )


@app.get("/videos/{video_name}")
async def get_video(video_name: str) -> FileResponse:
    """Checks the availabillity of a specific video 

    Parameters
    ----------
    video_name : str
        File name of the wanted video

    Returns
    -------
    FileResponse
        Returns the path, where the given video is located s
    """
    video_path = os.path.join(VIDEO_DIR, video_name)
    return FileResponse(video_path)


# @app.get('/list/a')
# async def list_videos():
#     videos = [f for f in os.listdir(
#         VIDEO_DIR) if f.endswith((".mp4", ".webm", ".ogg"))]
#     v_name = [f.split('.')[0] for f in videos]
#     return [
#         Video(name=v_name[i], path=videos[i]) for i in range(len(videos))
#     ]


@ app.get("/add")
async def add_video() -> HTMLResponse:
    """Add a video manually to the list

    Returns
    -------
    HTMLResponse
        HTML page providing the tools, to add a video manually to the list
    """
    return HTMLResponse(content=ADD_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)

# @app.get("/download", response_class=HTMLResponse)
# async def download_video() -> HTMLResponse:
#     """Provides a HTML page where a video url text field is provided"""
#     return HTMLResponse(content=DOWNLOAD_HTML_FILE_CONTENT, status_code=status.HTTP_201_CREATED)

# @app.put("/download")
# async def download_via_url(url_model: URL) -> HTMLResponse:
#     """Runs a background command that downloads the given video and puts it into the library"""
#     try:
#         background_command = [
#             'yt-dlp',
#             '-o', os.path.join('OUTPUT_PATH', '%(title)s.%(ext)s'),
#             url_model.url,
#         ]
#         subprocess.run(background_command, check=True)
#         return HTMLResponse(content=f"Video {url_model.url} downloaded successfully", status_code=201)
#     except subprocess.CalledProcessError as error:
#         raise HTTPException(status_code=400, detail=str(error))

@app.get("/download")
async def download_video() -> HTMLResponse:
    """Provides a HTML page where a video url text field is provided

    Returns
    -------
    HTMLResponse
        HTML page
    """
    return HTMLResponse(content=DOWNLOAD_HTML_FILE_CONTENT, status_code=status.HTTP_201_CREATED)


@app.put("/download")
async def download_video_via_url(url_model: URL) -> HTMLResponse:
    """Runs a background command that downloads the given video and puts it into the library 

    Parameters
    ----------
    url_model : URL
        gets the URL, that was given in the textflied in download.html 

    Returns
    -------
    HTMLResponse
        returns massage in terminal if video was downloadet successfully

    Raises
    ------
    HTTPException
        if something goes wrong, raise error 
    """
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

        # raise HTTPException(status_code=400, detail=str(error))


# TODO if is used in server, add docstring (as above) or comment out/remove
@app.post("/submit")
async def submit(request: Request) -> HTMLResponse:
    data = await request.json()
    text_value = data.get("text")
    print(f"Received text: {text_value}")

    return HTMLResponse(
        content={"message": "Text received", "text": text_value},
        status_code=status.HTTP_201_CREATED
    )

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
