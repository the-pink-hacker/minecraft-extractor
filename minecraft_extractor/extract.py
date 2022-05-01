import logging
import os.path
import shutil
from zipfile import ZipFile

from minecraft_extractor.minecraft import MinecraftVersion
from minecraft_extractor.settings import MAIN_SETTINGS
from minecraft_extractor.util.console import get_logger


class Extractor:
    version: MinecraftVersion
    out_dir: str
    temp_dir: str
    logger: logging.Logger

    def __init__(self, version: str):
        self.version = MinecraftVersion(version)
        self.out_dir = MAIN_SETTINGS.get_property("locations", "out")
        self.temp_dir = MAIN_SETTINGS.get_property("locations", "temp")
        self.logger = get_logger("Extract", str(self.version))

    def run(self):
        # Setup temp dir
        if os.path.exists(self.temp_dir):
            self.clear_temp()

        self.extract_indexed_assets()
        self.extract_jar()
        self.package()

    def extract_indexed_assets(self):
        assets = self.version.get_assets()

        logger = get_logger(self.logger.name, "Indexed")

        for i, asset in enumerate(assets, start=1):
            asset_dir = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"),
                                     "assets",
                                     "objects",
                                     asset.asset_hash[:2],
                                     asset.asset_hash)
            asset_temp_dir = os.path.join(self.temp_dir, "assets", asset.file)
            asset.download()

            # Copy to temp dir
            try:
                shutil.copyfile(asset_dir, asset_temp_dir)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(asset_temp_dir))
                shutil.copyfile(asset_dir, asset_temp_dir)

            logger.info(f"Extracted asset [{i}/{len(assets)}]: assets/{asset.file}")

    def extract_jar(self):
        logger = get_logger(self.logger.name, "Jar")

        self.version.download_jar()

        with ZipFile(self.version.jar_dir, "r") as jar:
            for i, archive_file in enumerate(jar.filelist, start=1):
                jar.extract(archive_file, self.temp_dir)
                logger.info(f"Extracted asset [{i}/{len(jar.filelist)}]: {archive_file.filename}")

    def package(self):
        pass

    def clear_temp(self):
        shutil.rmtree(self.temp_dir)
