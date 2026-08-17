"""Base entity class for coolify_monitor."""

from typing import TYPE_CHECKING

from custom_components.coolify_monitor.const import ATTRIBUTION
from custom_components.coolify_monitor.coordinator import CoolifyMonitorDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class CoolifyMonitorEntity(CoordinatorEntity[CoolifyMonitorDataUpdateCoordinator]):
    """
    Base entity providing device info, unique ID and attribution.

    The unique ID is `{entry_id}_{key}`, the documented identifier of last resort.
    A real integration switches to the device's serial, MAC or account ID before its
    first release, because changing it afterwards needs a registry migration.

    Every entity is grouped under one placeholder device for the whole config entry.
    This is temporary: once real sensor/binary_sensor entities exist, each Coolify
    resource (server, application, database) becomes its own device, and this class
    is rebuilt to take a resource kind and UUID instead of assuming a single device.
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CoolifyMonitorDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            name=coordinator.config_entry.title,
            manufacturer="Coolify",
        )
