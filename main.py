import logging
import sys

from minecraft_extractor import minecraft
from minecraft_extractor.extract import Extractor
from minecraft_extractor.settings import MAIN_SETTINGS
from minecraft_extractor.util import folder_dialog


def main():
    setup_logger()
    setup_settings()
    minecraft.init()

    Extractor("1.18.2").run()


def setup_logger():
    logging.basicConfig(
        format="[\x1b[32m%(asctime)s\x1b[0m] [\x1b[34m%(name)s\x1b[0m] "
               "[\x1b[33m%(levelname)s\x1b[0m] \x1b[36m%(message)s\x1b[0m",
        datefmt="%H:%M:%S",
        level=logging.INFO
    )


def setup_settings():
    """
    Sets up any settings that require user input to decide the default
    """
    # Minecraft
    if MAIN_SETTINGS.is_property_unset("locations", "minecraft"):
        if sys.platform == "windows":
            minecraft_dir = folder_dialog(title="Select Minecraft directory", directory="%APPDATA%/.minecraft")
        else:
            minecraft_dir = folder_dialog(title="Select Minecraft directory", directory="~/.minecraft")
        MAIN_SETTINGS.set_property("locations", "minecraft", minecraft_dir)

    MAIN_SETTINGS.save()


if __name__ == "__main__":
    main()
