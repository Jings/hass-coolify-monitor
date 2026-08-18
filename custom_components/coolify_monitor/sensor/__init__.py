"""Sensor platform for coolify_monitor."""

from typing import TYPE_CHECKING

from .application import ENTITY_DESCRIPTIONS as APPLICATION_ENTITY_DESCRIPTIONS
from .entity import CoolifyMonitorSensor

# Read-only platform: the coordinator already serializes the fetch.
PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from custom_components.coolify_monitor.data import CoolifyMonitorConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoolifyMonitorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        CoolifyMonitorSensor(coordinator, description, resource_kind="applications", resource_uuid=uuid)
        for uuid in coordinator.data["applications"]
        for description in APPLICATION_ENTITY_DESCRIPTIONS
    )
