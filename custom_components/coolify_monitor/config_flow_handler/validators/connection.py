"""Connection validation for the config flow."""

from typing import TYPE_CHECKING

from custom_components.coolify_monitor.api import CoolifyMonitorApiClient, CoolifyMonitorApiClientError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_connection(hass: HomeAssistant, url: str, api_token: str) -> str:
    """
    Test the connection and find this instance's stable identifier.

    Returns:
        The uuid of the server Coolify itself runs on, used as the config entry's unique ID.

    Raises:
        CoolifyMonitorApiClientAuthenticationError: If the API token is rejected.
        CoolifyMonitorApiClientCommunicationError: If the API cannot be reached.
        CoolifyMonitorApiClientError: If no server is flagged as the Coolify host.

    """
    client = CoolifyMonitorApiClient(
        base_url=url,
        api_token=api_token,
        session=async_get_clientsession(hass),
    )
    servers = await client.async_get_servers()

    for server in servers:
        if server.get("is_coolify_host"):
            return server["uuid"]

    msg = "No server in this Coolify instance is flagged as the Coolify host"
    raise CoolifyMonitorApiClientError(msg)


__all__ = ["validate_connection"]
