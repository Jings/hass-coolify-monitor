"""Base entity class for coolify_monitor."""

from typing import TYPE_CHECKING

from custom_components.coolify_monitor.const import ATTRIBUTION
from custom_components.coolify_monitor.coordinator import (
    CoolifyMonitorDataUpdateCoordinator,
    CoolifyMonitorResourceKind,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription

_DEVICE_MODEL_BY_KIND: dict[CoolifyMonitorResourceKind, str] = {
    "servers": "Server",
    "applications": "Application",
    "databases": "Database",
}


class CoolifyMonitorEntity(CoordinatorEntity[CoolifyMonitorDataUpdateCoordinator]):
    """
    Base entity for one Coolify resource, providing device info, unique ID and attribution.

    Every entity belongs to exactly one resource (a server, application or database) and
    is grouped under that resource's own device, rather than one device per config entry.
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CoolifyMonitorDataUpdateCoordinator,
        entity_description: EntityDescription,
        resource_kind: CoolifyMonitorResourceKind,
        resource_uuid: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.resource_kind = resource_kind
        self.resource_uuid = resource_uuid
        self._attr_unique_id = f"{resource_uuid}_{entity_description.key}"

        resource = coordinator.data[resource_kind][resource_uuid]
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.domain, resource_uuid)},
            name=resource["name"],
            manufacturer="Coolify",
            model=_DEVICE_MODEL_BY_KIND[resource_kind],
        )
