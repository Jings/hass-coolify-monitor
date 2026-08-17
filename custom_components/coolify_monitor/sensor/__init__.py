"""Sensor platform for coolify_monitor."""

from typing import TYPE_CHECKING

from .entity import CoolifyMonitorSensor, CoolifyMonitorSensorEntityDescription

# Read-only platform: the coordinator already serializes the fetch.
PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from custom_components.coolify_monitor.data import CoolifyMonitorConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorSensorEntityDescription, ...] = ()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoolifyMonitorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        CoolifyMonitorSensor(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )
