import json

class AssetManifest:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self._load()

    def _load(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except Exception as e:
            raise RuntimeError(f"Failed to load manifest: {e}")

    def get_asset(self, category, name):
        """Retrieve the file path of an asset."""
        try:
            return self.data[category][name]
        except KeyError:
            raise ValueError(f"Asset '{name}' not found in category '{category}'.")
