"""This module is the starting point of the `Media-Server` side"""
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="static/templates")

DOWNLOAD_HTML_FILE_PATH: Path = Path("static/templates/download.html")
assert DOWNLOAD_HTML_FILE_PATH.exists(), "download.html not found"
DOWNLOAD_HTML_FILE_CONTENT: str = DOWNLOAD_HTML_FILE_PATH.read_text(
    encoding="utf-8")
assert len(
    DOWNLOAD_HTML_FILE_CONTENT) > 0, "download.html content could not be loaded"

OUTPUT_PATH: str = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
assert len(OUTPUT_PATH) > 0, "invalid output path"

INDEX_HTML_FILE_PATH: Path = Path("static/templates/index.html")
INDEX_HTML_FILE_CONTENT: str = INDEX_HTML_FILE_PATH.read_text(encoding="utf-8")
assert INDEX_HTML_FILE_PATH.exists(), "index.html not found"

TEAPOT_HTML_FILE_PATH: Path = Path("static/templates/teapot.html")
TEAPOT_HTML_FILE_CONTENT: str = TEAPOT_HTML_FILE_PATH.read_text(
    encoding='utf-8')
assert TEAPOT_HTML_FILE_PATH.exists(), 'teapot.html not found'

LOADING_HTML_FILE_PATH: Path = Path("static/templates/loading.html")
LOADING_HTML_FILE_CONTENT: str = LOADING_HTML_FILE_PATH.read_text(
    encoding="utf-8")
assert LOADING_HTML_FILE_PATH.exists(), "loading.html not found"

LIST_HTML_FILE_PATH: Path = Path("static/templates/list.html")
assert LIST_HTML_FILE_PATH.exists(), "list.html not found"
LIST_HTML_FILE_CONTENT: str = LIST_HTML_FILE_PATH.read_text(encoding="utf-8")
assert len(LIST_HTML_FILE_CONTENT) > 0, "list.html content could not be loaded"

EASTEREGG_HTML_FILE_PATH: Path = Path("static/templates/easteregg.html")
EASTEREGG_HTML_FILE_CONTENT: str = EASTEREGG_HTML_FILE_PATH.read_text(encoding="utf-8")
assert EASTEREGG_HTML_FILE_PATH.exists(), "easteregg.html not found"

ADD_HTML_FILE_PATH: Path = Path("static/templates/listAddManually.html")
assert ADD_HTML_FILE_PATH.exists(), "listAddManually.html not found"
ADD_HTML_FILE_CONTENT: str = ADD_HTML_FILE_PATH.read_text(encoding="utf-8")
assert (
    len(ADD_HTML_FILE_CONTENT) > 0
), "listAddManually.html content could not be loaded"


VIDEO_DIR: str = "downloads"

video_db: list[Video] = []
for video_file in os.listdir(VIDEO_DIR):
    if video_file.endswith(".mp4") or video_file.endswith(".webm"):
        video = Video(name=video_file, path=os.path.join(
            VIDEO_DIR, video_file))
        video_db.append(video)


class TeapotException(HTTPException):
    def __init__(self, detail=None, headers: Dict[str, str] | None = None) -> None:
        super().__init__(418, detail, headers)


@app.exception_handler(TeapotException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # TODO add teapot here
    html_content = """
    <html>
        <head>
            <title>418 Method Not Allowed</title>
        </head>
        <body>
            <h1>418 Method Not Allowed</h1>
            <p>The method is not allowed for the requested URL.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=exc.status_code)


@app.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def read_root() -> HTMLResponse:
    """Homepage

    Returns
    -------
    HTMLResponse
        A HTML Page consisting every important redirect
    """
    return HTMLResponse(content=INDEX_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)

@app.get(
    path="/easteregg",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def read_easteregg() -> HTMLResponse:
    return HTMLResponse(content=EASTEREGG_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)

@app.get("/teapot", response_class=HTMLResponse)
async def teapot_page() -> HTMLResponse:
    return HTMLResponse(content=TEAPOT_HTML_FILE_CONTENT, status_code=418)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return HTMLResponse(content=TEAPOT_HTML_FILE_CONTENT, status_code=418)


@app.post(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_418_IM_A_TEAPOT,
)
async def teapot() -> HTMLResponse:
    """Homepage

    Returns
    -------
    HTMLResponse
        A HTML Page consisting every important redirect
    """
    raise TeapotException("root")


@app.get(path="/list", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def list_videos_get_method(request: Request) -> HTMLResponse:
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
    videos = [
        {"name": f.split(".")[0], "path": f"/videos/{f}"}
        for f in os.listdir(VIDEO_DIR)
        if f.endswith((".mp4", ".webm", ".ogg"))
    ]

    return templates.TemplateResponse(
        request=request,
        name="list.html",
        context={"videos": videos},
        status_code=status.HTTP_200_OK,
    )


@app.get("/videos/{video_name}", response_class=FileResponse)
async def get_video(video_name: str) -> FileResponse:
    """Checks the availabillity of a specific video

    Parameters
    ----------
    video_name : str
        File name of the wanted video

    Returns
    -------
    FileResponse
        Returns the path, where the given video is located
    """
    # TODO in case the video is not in the database, return a 404 or something
    video_path = os.path.join(VIDEO_DIR, video_name)
    return FileResponse(video_path)


@app.get(
    path="/download", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED
)
async def download_video_get_method() -> HTMLResponse:
    """Provides a HTML page where a video url text field is provided

    Returns
    -------
    HTMLResponse
        HTML page
    """
    return HTMLResponse(
        content=DOWNLOAD_HTML_FILE_CONTENT, status_code=status.HTTP_201_CREATED
    )


@app.get(path="/loading", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def loading_page_get_method() -> HTMLResponse:
    """Provides a HTML page where a loading animation and redirect buttons are provided

    Returns
    -------
    HTMLResonse
        HTML page
    """
    return HTMLResponse(
        content=LOADING_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK
    )


@app.put(
    path="/download", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED
)
async def download_video_put_method(url_model: URL) -> HTMLResponse:
    """Runs a background command that downloads the given video and puts it into the library

    Parameters
    ----------
    url_model : URL
        gets the URL, that was given in the textflied in download.html

    Returns
    -------
    HTMLResponse
        returns massage in terminal if video was downloaded successfully

    Raises
    ------
    HTTPException
        if something goes wrong, raise error
    """
    try:
        background_command = [
            "yt-dlp",
            "-o",
            os.path.join(OUTPUT_PATH, "%(title)s.%(ext)s"),
            url_model.url,
        ]
        subprocess.run(background_command, check=True)

        return HTMLResponse(
            content=f"Video {url_model.url} downloaded successfully",
            status_code=status.HTTP_201_CREATED,
        )

    except subprocess.CalledProcessError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error


@app.get("/list")
async def video_list() -> HTMLResponse:
    return HTMLResponse(content=LIST_HTML_FILE_CONTENT, status_code=status.HTTP_200_OK)
