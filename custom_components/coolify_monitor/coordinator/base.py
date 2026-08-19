"""Data update coordinator for coolify_monitor."""

import asyncio
from typing import TYPE_CHECKING, Any

from custom_components.coolify_monitor.api import (
    CoolifyMonitorApiClientAuthenticationError,
    CoolifyMonitorApiClientError,
)
from custom_components.coolify_monitor.const import CONF_SELECTED_RESOURCES, DOMAIN
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .models import CoolifyMonitorCoordinatorData
from .transform import build_coordinator_data, filter_to_selected

if TYPE_CHECKING:
    from custom_components.coolify_monitor.data import CoolifyMonitorConfigEntry


async def _empty_list() -> list[Any]:
    """
    Stand in for a skipped API call.

    Returns:
        An empty list, as if the endpoint had returned no resources.

    """
    return []


async def _no_version() -> str | None:
    """
    Stand in for a skipped version fetch.

    Returns:
        None, as if no version had been fetched.

    """
    return None


class CoolifyMonitorDataUpdateCoordinator(DataUpdateCoordinator[CoolifyMonitorCoordinatorData]):
    """Fetch every monitored Coolify resource once per interval and hand it to every entity."""

    config_entry: CoolifyMonitorConfigEntry

    async def _async_update_data(self) -> CoolifyMonitorCoordinatorData:
        """
        Fetch servers, applications, databases, teams and services from the Coolify API.

        Returns:
            Every selected resource, grouped by kind and keyed by UUID.

        Raises:
            ConfigEntryAuthFailed: If the API token was rejected; triggers reauth.
            UpdateFailed: If the fetch failed for any other reason.

        """
        client = self.config_entry.runtime_data.client
        selected = self.config_entry.options.get(CONF_SELECTED_RESOURCES)
        fetch_servers = selected is None or selected["servers"]

        try:
            servers, applications, databases, teams, services, version = await asyncio.gather(
                client.async_get_servers() if fetch_servers else _empty_list(),
                client.async_get_applications() if selected is None or selected["applications"] else _empty_list(),
                client.async_get_databases() if selected is None or selected["databases"] else _empty_list(),
                client.async_get_teams() if selected is None or selected["teams"] else _empty_list(),
                client.async_get_services() if selected is None or selected["services"] else _empty_list(),
                client.async_get_version() if fetch_servers else _no_version(),
            )
        except CoolifyMonitorApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(
                translation_domain=DOMAIN,
                translation_key="authentication_failed",
            ) from exception
        except CoolifyMonitorApiClientError as exception:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
            ) from exception

        data = build_coordinator_data(servers, applications, databases, teams, services, version)
        if selected is not None:
            data = filter_to_selected(data, selected)
        return data
