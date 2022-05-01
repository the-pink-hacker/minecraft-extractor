import logging
import os.path
import shutil
from typing import Optional
from zipfile import ZipFile, ZipInfo

from minecraft_extractor.minecraft import MinecraftVersion, IndexedAsset
from minecraft_extractor.settings import MAIN_SETTINGS
from minecraft_extractor.util.console import get_logger


class Extractor:
    version: MinecraftVersion
    extract: list[str]
    out_dir: str
    temp_dir: str
    logger: logging.Logger

    def __init__(self, version: str, extract: list[str]):
        self.version = MinecraftVersion(version)
        self.extract = extract
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

        filtered_assets = list(filter(self.should_extract_indexed_asset, assets))

        for i, asset in enumerate(filtered_assets, start=1):
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

            if i % 100 == 0 or i == len(filtered_assets):
                logger.info(f"Extracted asset [{i}/{len(filtered_assets)}]")

    def extract_jar(self):
        logger = get_logger(self.logger.name, "Jar")

        self.version.download_jar()

        with ZipFile(self.version.jar_dir, "r") as jar:
            filtered_file_list = list(filter(self.should_extract_asset, jar.filelist))
            for i, archive_file in enumerate(filtered_file_list, start=1):
                jar.extract(archive_file, self.temp_dir)

                if i % 100 == 0 or i == len(filtered_file_list):
                    logger.info(f"Extracted file [{i}/{len(filtered_file_list)}]")

    def package(self):
        pass

    def clear_temp(self):
        shutil.rmtree(self.temp_dir)

    def should_extract_asset(self, file: ZipInfo) -> Optional[ZipInfo]:
        if self.extract == ["*"]:
            return file

        for extract in self.extract:
            if file.filename.startswith(extract):
                return file
        return None

    def should_extract_indexed_asset(self, asset: IndexedAsset) -> Optional[IndexedAsset]:
        if self.extract == ["*"]:
            return asset

        for extract in self.extract:
            if os.path.join("assets", asset.file).startswith(extract):
                return asset
        return None
