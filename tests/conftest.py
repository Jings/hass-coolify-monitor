"""Shared fixtures for the coolify_monitor tests."""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.coolify_monitor.const import DOMAIN
from homeassistant.const import CONF_API_TOKEN, CONF_URL
from homeassistant.core import HomeAssistant

HOST_SERVER_UUID = "demo-server-uuid"
_HOST_SERVER_REF = {"uuid": HOST_SERVER_UUID, "name": "localhost"}

SERVERS_RESPONSE: list[dict[str, Any]] = [
    {
        "uuid": HOST_SERVER_UUID,
        "name": "localhost",
        "description": "Demo server",
        "is_reachable": True,
        "is_usable": True,
        "is_coolify_host": True,
    },
]

APPLICATIONS_RESPONSE: list[dict[str, Any]] = [
    {
        "uuid": "demo-app-uuid",
        "name": "demo-app",
        "description": "Demo application",
        "status": "running:healthy",
        "fqdn": "https://demo.example.com",
        "git_repository": "demo/app",
        "git_branch": "main",
        "destination": {"server": _HOST_SERVER_REF},
    },
]

DATABASES_RESPONSE: list[dict[str, Any]] = [
    {
        "uuid": "demo-db-uuid",
        "name": "demo-db",
        "description": "Demo database",
        "status": "running:healthy",
        "database_type": "standalone-postgresql",
        "image": "postgres:17-alpine",
        "destination": {"server": _HOST_SERVER_REF},
    },
]

VERSION_RESPONSE = "4.0.0-beta.442"

_RESPONSES_BY_PATH: dict[str, Any] = {
    "/servers": SERVERS_RESPONSE,
    "/applications": APPLICATIONS_RESPONSE,
    "/databases": DATABASES_RESPONSE,
    "/version": VERSION_RESPONSE,
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load custom integrations in every test."""


@pytest.fixture
def mock_api() -> Generator[AsyncMock]:
    """Replace the client's HTTP layer, returning canned resource lists."""

    async def _respond(method: str, path: str, decode: str = "json") -> Any:
        return _RESPONSES_BY_PATH[path]

    with patch(
        "custom_components.coolify_monitor.api.client.CoolifyMonitorApiClient._api_wrapper",
        new_callable=AsyncMock,
        side_effect=_respond,
    ) as api_wrapper:
        yield api_wrapper


@pytest.fixture
def config_entry() -> MockConfigEntry:
    """Return a config entry for this integration."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="https://demo.example.com",
        unique_id=HOST_SERVER_UUID,
        data={CONF_URL: "https://demo.example.com", CONF_API_TOKEN: "secret"},
    )


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> MockConfigEntry:
    """
    Set up the integration from a config entry.

    Returns:
        The config entry, now loaded.

    """
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
