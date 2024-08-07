

def download_video_from_url(url: str) -> bool:
    """Download video from given URL

    Parameters
    ----------
    url : str
        the videos URL

    Returns
    -------
    bool
        return `True` if the download was successful, else return `False`
    """
    # TODO check if video was already downloaded before (check with URL)
    # TODO download video
    # TODO once downloaded, add to video_db
    # TODO convert to .mp4 if necessary

    # only return True if the download was successful
    # os.system(url)

    return True


def encode_video(video_file_path: str) -> bool:
    """Loads the video from the file path and encodes it into multiple representations

    Parameters
    ----------
    video_file_path : str
        the location of the video file on the server

    Returns
    -------
    bool
        return `True` if the video could be encoded, else return `False`
    """
    # TODO encode the video into multiple representations

    # only return True if the encoding was successful
    return True
