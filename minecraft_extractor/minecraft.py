import json
import os.path
from dataclasses import dataclass, asdict

from minecraft_extractor.settings import MAIN_SETTINGS
from minecraft_extractor.util.files import download_file

_VERSION_MANIFEST = "version_manifest_v2.json"
_VERSION_MANIFEST_URL = f"https://launchermeta.mojang.com/mc/game/{_VERSION_MANIFEST}"

_INDEXED_ASSET_URL = "https://resources.download.minecraft.net"

_PARSED_VERSION_MANIFEST: dict


def update_version_manifest():
    download_file(_VERSION_MANIFEST_URL,
                  os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"), "versions", _VERSION_MANIFEST),
                  check_out=not MAIN_SETTINGS.get_property("indexes", "update_version_manifest"))


def parse_version_manifest() -> dict:
    version_manifest = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"), "versions", _VERSION_MANIFEST)

    with open(version_manifest, "r") as file:
        return json.load(file)


def init():
    update_version_manifest()

    global _PARSED_VERSION_MANIFEST
    _PARSED_VERSION_MANIFEST = parse_version_manifest()


class IndexedAsset:
    file: str
    asset_hash: str

    def __init__(self, file: str, asset_hash: str):
        self.file = file
        self.asset_hash = asset_hash

    def download(self):
        asset_dir = os.path.join(self.asset_hash[:2], self.asset_hash)
        download_file(f"{_INDEXED_ASSET_URL}/{asset_dir}",
                      os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"),
                                   "assets",
                                   "objects",
                                   asset_dir),
                      check_out=True)

    def __str__(self) -> str:
        return self.file

    def __repr__(self) -> str:
        return str(self)


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
        download_file(self.manifest_entry["url"], version_index_dir, check_out=True)

        with open(version_index_dir, "r") as file:
            self.version_index = json.load(file)

        # Asset index
        asset_index_dir = os.path.join(MAIN_SETTINGS.get_property("locations", "minecraft"),
                                       "assets",
                                       "indexes",
                                       f"{self.version_index['assetIndex']['id']}.json")
        download_file(self.version_index["assetIndex"]["url"], asset_index_dir, check_out=True)

        with open(asset_index_dir, "r") as file:
            self.asset_index = json.load(file)

    def get_assets(self) -> list[IndexedAsset]:
        assets = []

        for file, asset in self.asset_index["objects"].items():
            assets.append(IndexedAsset(file, asset["hash"]))

        return assets

    def download(self):
        pass

    def __str__(self) -> str:
        return self.version_id

    def __repr__(self) -> str:
        return str(asdict(self))

    @staticmethod
    def get_latest_release() -> "MinecraftVersion":
        """
        Gets the latest release version according to the version manifest

        :return: The latest version
        """
        return MinecraftVersion(_PARSED_VERSION_MANIFEST["latest"]["release"])

    @staticmethod
    def get_latest_snapshot() -> "MinecraftVersion":
        """
        Gets the latest snapshot version according to the version manifest

        :return: The latest version
        """
        return MinecraftVersion(_PARSED_VERSION_MANIFEST["latest"]["snapshot"])
