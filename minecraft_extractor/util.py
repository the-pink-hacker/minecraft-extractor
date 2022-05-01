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


def download_file(url: str, dest: str):
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    with requests.get(url, stream=True) as r:
        with open(dest, "wb") as f:
            shutil.copyfileobj(r.raw, f)
