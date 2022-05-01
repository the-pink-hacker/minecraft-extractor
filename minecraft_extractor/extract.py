import logging
import os.path
import shutil

from minecraft_extractor.minecraft import MinecraftVersion
from minecraft_extractor.settings import MAIN_SETTINGS


class Extractor:
    version: MinecraftVersion
    out_dir: str
    temp_dir: str
    logger: logging.Logger

    def __init__(self, version: str):
        self.version = MinecraftVersion(version)
        self.out_dir = MAIN_SETTINGS.get_property("locations", "out")
        self.temp_dir = MAIN_SETTINGS.get_property("locations", "temp")
        self.logger = logging.getLogger("Extract")

    def run(self):
        # Setup temp dir
        if os.path.exists(self.temp_dir):
            self.clear_temp()

        self.extract_indexed_assets()
        self.extract_jar()

    def extract_indexed_assets(self):
        assets = self.version.get_assets()
        logging.info("Extracting indexed assets...")
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

            self.logger.info(f"Extracted asset [{i}/{len(assets)}]: {asset.file}")

    def extract_jar(self):
        pass

    def clear_temp(self):
        shutil.rmtree(self.temp_dir)
