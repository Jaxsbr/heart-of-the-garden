from core.resources.asset_loader import load_texture
from core.resources.resource_type import ResourceType

class ResourceManager:
    def __init__(self):
        self.cache = {}

    def load(self, resource_type, name, path, scale_size):
        if name not in self.cache:
            self.cache[name] = self._load_resource(resource_type, path, scale_size)
        return self.cache[name]

    def unload(self, name):
        if name in self.cache:
            del self.cache[name]

    def _load_resource(self, resource_type, path, scale_size):
        match resource_type:
            case ResourceType.TEXTURE:
                return load_texture(path, scale_size)
        print(f"resource type not implemented: {resource_type}")
