"""Sensor platform for coolify_monitor."""

from itertools import chain
from typing import TYPE_CHECKING

from .application import ENTITY_DESCRIPTIONS as APPLICATION_ENTITY_DESCRIPTIONS
from .database import ENTITY_DESCRIPTIONS as DATABASE_ENTITY_DESCRIPTIONS
from .entity import CoolifyMonitorSensor
from .server import ENTITY_DESCRIPTIONS as SERVER_ENTITY_DESCRIPTIONS

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
        chain(
            (
                CoolifyMonitorSensor(coordinator, description, resource_kind="servers", resource_uuid=uuid)
                for uuid in coordinator.data["servers"]
                for description in SERVER_ENTITY_DESCRIPTIONS
            ),
            (
                CoolifyMonitorSensor(coordinator, description, resource_kind="applications", resource_uuid=uuid)
                for uuid in coordinator.data["applications"]
                for description in APPLICATION_ENTITY_DESCRIPTIONS
            ),
            (
                CoolifyMonitorSensor(coordinator, description, resource_kind="databases", resource_uuid=uuid)
                for uuid in coordinator.data["databases"]
                for description in DATABASE_ENTITY_DESCRIPTIONS
            ),
        ),
    )
