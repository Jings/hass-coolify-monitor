"""
Custom integration to integrate coolify_monitor with Home Assistant.

For more details about this integration, please refer to:
https://github.com/Jings/hass-coolify-monitor
"""

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_API_TOKEN, CONF_URL, Platform
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import CoolifyMonitorApiClient
from .const import CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES, DOMAIN, LOGGER
from .coordinator import CoolifyMonitorDataUpdateCoordinator
from .data import CoolifyMonitorData
from .entity_utils import build_device_info
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import CoolifyMonitorConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Register the service actions.

    Returns:
        True once the actions are registered.

    """
    await async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoolifyMonitorConfigEntry,
) -> bool:
    """
    Set up a config entry.

    Returns:
        True once the coordinator has data and every platform is forwarded.

    """
    client = CoolifyMonitorApiClient(
        base_url=entry.data[CONF_URL],
        api_token=entry.data[CONF_API_TOKEN],
        session=async_get_clientsession(hass),
    )

    interval_minutes = int(entry.options.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES))
    coordinator = CoolifyMonitorDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=timedelta(minutes=interval_minutes),
        always_update=False,
    )

    entry.runtime_data = CoolifyMonitorData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    device_registry = dr.async_get(hass)
    for server_uuid, server in coordinator.data["servers"].items():
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            **build_device_info(entry.domain, "servers", server_uuid, name=server["name"]),
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: CoolifyMonitorConfigEntry,
) -> bool:
    """
    Unload a config entry.

    Returns:
        True if every platform unloaded cleanly.

    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: CoolifyMonitorConfigEntry,
) -> None:
    """Reload the config entry after its data or options changed."""
    await hass.config_entries.async_reload(entry.entry_id)
