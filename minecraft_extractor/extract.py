from minecraft_extractor.minecraft import MinecraftVersion, update_version_manifest


class Extractor:
    out_dir: str
    version: MinecraftVersion

    def __init__(self, version: str):
        self.version = MinecraftVersion(version)

    def run(self):
        print(self.version)

        # Extract indexed assets

        # Extract jar
