import json
import os.path
from dataclasses import dataclass, asdict

from minecraft_extractor.settings import MAIN_SETTINGS
from minecraft_extractor.util import download_file

_VERSION_MANIFEST = "version_manifest_v2.json"
_VERSION_MANIFEST_URL = f"https://launchermeta.mojang.com/mc/game/{_VERSION_MANIFEST}"

_INDEXED_ASSET_URL = "https://launchermeta.mojang.com"

_PARSED_VERSION_MANIFEST: dict


def update_version_manifest():
    download_file(_VERSION_MANIFEST_URL,
                  os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"), "versions", _VERSION_MANIFEST))


def parse_version_manifest() -> dict:
    version_manifest = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"), "versions", _VERSION_MANIFEST)

    with open(version_manifest, "r") as file:
        return json.load(file)


def init():
    update_version_manifest()

    global _PARSED_VERSION_MANIFEST
    _PARSED_VERSION_MANIFEST = parse_version_manifest()


@dataclass
class MinecraftVersion:
    version_id: str
    manifest_entry: dict
    version_index: dict
    asset_index: dict

    def __init__(self, version_id: str):
        self.version_id = version_id

        # Manifest Entry
        for version in _PARSED_VERSION_MANIFEST["versions"]:
            if self.version_id == version["id"]:
                self.manifest_entry = version
                break

        # Version index
        version_index_dir = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"),
                                         "versions",
                                         self.manifest_entry["id"],
                                         f"{self.manifest_entry['id']}.json")
        download_file(self.manifest_entry["url"], version_index_dir)

        with open(version_index_dir, "r") as file:
            self.version_index = json.load(file)

        # Asset index
        asset_index_dir = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"),
                                       "assets",
                                       "indexes",
                                       f"{self.version_index['assetIndex']['id']}.json")
        download_file(self.version_index["assetIndex"]["url"], asset_index_dir)

        with open(asset_index_dir, "r") as file:
            self.asset_index = json.load(file)

    def __str__(self):
        return self.version_id

    def __repr__(self):
        return str(asdict(self))

    @staticmethod
    def get_latest() -> "MinecraftVersion":
        """
        Gets the latest version according to the version manifest

        :return: The latest version
        """
        pass
