import logging
import os
import shutil
from tkinter import filedialog

import requests as requests


def parse_dir(directory):
    return os.path.normpath(os.path.abspath(os.path.expanduser(directory)))


def folder_dialog(title="Select Folder", directory=os.path.abspath(os.sep)):
    logging.info(f"Select Folder: {title}")
    return parse_dir(filedialog.askdirectory(title=title, initialdir=directory))


def download_file(url: str, out: str, check_out: bool = False):
    """
    Download a file from an url

    :param url: The url that the file is located at
    :param out: The directory that the file will be saved to
    :param check_out: Check if the out directory already exists
    """
    if check_out:
        if os.path.exists(out):
            return

    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    with requests.get(url, stream=True) as r:
        with open(out, "wb") as f:
            shutil.copyfileobj(r.raw, f)
