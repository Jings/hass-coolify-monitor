"""Build the device info shared by every Coolify resource's entities."""

from custom_components.coolify_monitor.coordinator import CoolifyMonitorResourceKind
from homeassistant.helpers.device_registry import DeviceInfo

_DEVICE_MODEL_BY_KIND: dict[CoolifyMonitorResourceKind, str] = {
    "servers": "Server",
    "applications": "Application",
    "databases": "Database",
}


def build_device_info(
    domain: str,
    resource_kind: CoolifyMonitorResourceKind,
    resource_uuid: str,
    name: str,
    via_device_id: str | None = None,
) -> DeviceInfo:
    """
    Build the device info for one Coolify resource.

    Args:
        domain: The config entry's domain, used in the device identifier.
        resource_kind: Which kind of Coolify resource this device represents.
        resource_uuid: The resource's UUID, used in the device identifier.
        name: The resource's own name, as reported by Coolify.
        via_device_id: The registry ID of the server this resource runs on, if any.

    Returns:
        The device info. Includes `via_device_id` only when one was given, so
        applications and databases show up as connected via their server. The
        device name is prefixed with its kind (e.g. "Server: localhost"),
        since Coolify resource names alone are often generic or identical
        across instances.

    """
    kind_label = _DEVICE_MODEL_BY_KIND[resource_kind]
    device_info = DeviceInfo(
        identifiers={(domain, resource_uuid)},
        name=f"{kind_label}: {name}",
        manufacturer="Coolify",
        model=kind_label,
    )
    if via_device_id is not None:
        device_info["via_device_id"] = via_device_id
    return device_info


__all__ = ["build_device_info"]
