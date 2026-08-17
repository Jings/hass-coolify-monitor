"""Data update coordinator for coolify_monitor."""

import asyncio
from typing import TYPE_CHECKING

from custom_components.coolify_monitor.api import (
    CoolifyMonitorApiClientAuthenticationError,
    CoolifyMonitorApiClientError,
)
from custom_components.coolify_monitor.const import DOMAIN
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .models import CoolifyMonitorCoordinatorData
from .transform import build_coordinator_data

if TYPE_CHECKING:
    from custom_components.coolify_monitor.data import CoolifyMonitorConfigEntry


class CoolifyMonitorDataUpdateCoordinator(DataUpdateCoordinator[CoolifyMonitorCoordinatorData]):
    """Fetch every monitored Coolify resource once per interval and hand it to every entity."""

    config_entry: CoolifyMonitorConfigEntry

    async def _async_update_data(self) -> CoolifyMonitorCoordinatorData:
        """
        Fetch servers, applications and databases from the Coolify API.

        Returns:
            Every resource, grouped by kind and keyed by UUID.

        Raises:
            ConfigEntryAuthFailed: If the API token was rejected; triggers reauth.
            UpdateFailed: If the fetch failed for any other reason.

        """
        client = self.config_entry.runtime_data.client
        try:
            servers, applications, databases = await asyncio.gather(
                client.async_get_servers(),
                client.async_get_applications(),
                client.async_get_databases(),
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

        return build_coordinator_data(servers, applications, databases)
