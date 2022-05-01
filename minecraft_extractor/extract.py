import os.path

from minecraft_extractor.minecraft import MinecraftVersion
from minecraft_extractor.settings import MAIN_SETTINGS
from minecraft_extractor.util import download_file


class Extractor:
    out_dir: str
    temp_dir: str
    version: MinecraftVersion

    def __init__(self, version: str):
        self.version = MinecraftVersion(version)
        self.out_dir = MAIN_SETTINGS.get_property("locations", "out")
        self.temp_dir = MAIN_SETTINGS.get_property("locations", "temp")

    def run(self):
        self.extract_indexed_assets()
        self.extract_jar()

    def extract_indexed_assets(self):
        for asset in self.version.get_assets():
            asset_dir = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"),
                                     "assets",
                                     "objects",
                                     asset.asset_hash[:2],
                                     asset.asset_hash)
            asset.download()

    def extract_jar(self):
        pass
