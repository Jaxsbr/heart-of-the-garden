from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
from core.resources.resource_type import ResourceType


def get_texture_resource(
    asset_manifest: AssetManifest, resource_manager: ResourceManager, texture_name
):
    asset_entry = asset_manifest.get_asset("textures", texture_name)
    return resource_manager.load(
        ResourceType.TEXTURE,
        texture_name,
        asset_entry["path"],
        (asset_entry["scale_x"], asset_entry["scale_y"]),
    )
