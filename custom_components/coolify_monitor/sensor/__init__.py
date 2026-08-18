"""Sensor platform for coolify_monitor."""

from typing import TYPE_CHECKING

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
    # No sensor entities exist yet. sensor/entity.py already has the reusable
    # pattern; real descriptions land the same way binary_sensor's did.
    async_add_entities([])
