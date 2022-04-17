import logging
import os
from tkinter import filedialog


def parse_dir(directory):
    return os.path.normpath(os.path.abspath(os.path.expanduser(directory)))


def folder_dialog(title="Select Folder", directory=os.path.abspath(os.sep)):
    logging.info(f"Select Folder: {title}")
    return parse_dir(filedialog.askdirectory(title=title, initialdir=directory))
