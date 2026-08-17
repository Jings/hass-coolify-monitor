"""
Runtime data types for coolify_monitor.

Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import CoolifyMonitorApiClient
    from .coordinator import CoolifyMonitorDataUpdateCoordinator


type CoolifyMonitorConfigEntry = ConfigEntry[CoolifyMonitorData]


@dataclass
class CoolifyMonitorData:
    """Runtime data stored on the config entry after a successful setup."""

    client: CoolifyMonitorApiClient
    coordinator: CoolifyMonitorDataUpdateCoordinator
    integration: Integration
