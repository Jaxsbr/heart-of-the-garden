from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
from core.resources.resource_type import ResourceType


def get_texture_resource(
    asset_manifest: AssetManifest,
    resource_manager: ResourceManager,
    texture_name,
    scale_x: int | None = None,
    scale_y: int | None = None,
    texture_cache_name="",
):
    asset_entry = asset_manifest.get_asset("textures", texture_name)
    cache_name = texture_name if not texture_cache_name else texture_cache_name
    return resource_manager.load(
        ResourceType.TEXTURE,
        cache_name,
        asset_entry["path"],
        (
            (asset_entry["scale_x"] if scale_x is None else scale_x),
            (asset_entry["scale_y"] if scale_y is None else scale_y),
        ),
    )
