"""Discovery logic shared between the config flow and the options flow."""

import asyncio
from typing import TYPE_CHECKING

from custom_components.coolify_monitor.api import CoolifyMonitorApiClient
from custom_components.coolify_monitor.coordinator import CoolifyMonitorCoordinatorData
from custom_components.coolify_monitor.coordinator.transform import build_coordinator_data
from homeassistant.helpers.aiohttp_client import async_get_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def async_discover_resources(hass: HomeAssistant, url: str, api_token: str) -> CoolifyMonitorCoordinatorData:
    """
    Fetch every server, application, database, team and service from the Coolify instance.

    Returns:
        Every resource, grouped by kind and keyed by UUID.

    Raises:
        CoolifyMonitorApiClientAuthenticationError: If the API token is rejected.
        CoolifyMonitorApiClientCommunicationError: If the API cannot be reached.

    """
    client = CoolifyMonitorApiClient(
        base_url=url,
        api_token=api_token,
        session=async_get_clientsession(hass),
    )
    servers, applications, databases, teams, services = await asyncio.gather(
        client.async_get_servers(),
        client.async_get_applications(),
        client.async_get_databases(),
        client.async_get_teams(),
        client.async_get_services(),
    )
    return build_coordinator_data(servers, applications, databases, teams, services)


__all__ = ["async_discover_resources"]
