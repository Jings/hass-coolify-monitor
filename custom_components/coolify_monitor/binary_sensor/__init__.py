"""Binary sensor platform for coolify_monitor."""

from typing import TYPE_CHECKING

from .entity import CoolifyMonitorBinarySensor
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
    """Set up the binary_sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        CoolifyMonitorBinarySensor(coordinator, description, resource_kind="servers", resource_uuid=server_uuid)
        for server_uuid in coordinator.data["servers"]
        for description in SERVER_ENTITY_DESCRIPTIONS
    )
