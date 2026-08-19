"""Base entity class for coolify_monitor."""

from typing import TYPE_CHECKING, cast

from custom_components.coolify_monitor.const import ATTRIBUTION
from custom_components.coolify_monitor.coordinator import (
    CoolifyMonitorDataUpdateCoordinator,
    CoolifyMonitorResourceKind,
)
from custom_components.coolify_monitor.coordinator.models import (
    CoolifyMonitorApplicationData,
    CoolifyMonitorDatabaseData,
    CoolifyMonitorServiceData,
)
from custom_components.coolify_monitor.entity_utils import build_device_info
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


def _find_server_device_id(
    coordinator: CoolifyMonitorDataUpdateCoordinator,
    resource_kind: CoolifyMonitorResourceKind,
    resource: object,
) -> str | None:
    """
    Look up the registry ID of the server an application, database or service runs on.

    Returns:
        The server device's registry ID, or None for a resource with no server of its own.

    """
    if resource_kind in ("servers", "teams"):
        return None

    resource = cast("CoolifyMonitorApplicationData | CoolifyMonitorDatabaseData | CoolifyMonitorServiceData", resource)
    device = dr.async_get(coordinator.hass).async_get_device_by_identifier(
        identifier=(coordinator.config_entry.domain, resource["server_uuid"]),
        config_entry_id=coordinator.config_entry.entry_id,
    )
    return device.id if device else None


class CoolifyMonitorEntity(CoordinatorEntity[CoolifyMonitorDataUpdateCoordinator]):
    """
    Base entity for one Coolify resource, providing device info, unique ID and attribution.

    Every entity belongs to exactly one resource (a server, application, database, team or
    service) and is grouped under that resource's own device, rather than one device per
    config entry. An application, database or service device links back to its server via
    `via_device_id`.
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
        self._attr_device_info = build_device_info(
            coordinator.config_entry.domain,
            resource_kind,
            resource_uuid,
            name=resource["name"],
            via_device_id=_find_server_device_id(coordinator, resource_kind, resource),
        )
