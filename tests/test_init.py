"""Tests for integration setup, including device registry linking."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.coolify_monitor.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr


async def test_application_device_links_to_its_server(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """An application's device is connected via the server it runs on."""
    device_registry = dr.async_get(hass)
    server_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "demo-server-uuid"),
        init_integration.entry_id,
    )
    application_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "demo-app-uuid"),
        init_integration.entry_id,
    )

    assert server_device is not None
    assert application_device is not None
    assert application_device.via_device_id == server_device.id


async def test_database_device_links_to_its_server(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """A database's device is connected via the server it runs on."""
    device_registry = dr.async_get(hass)
    server_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "demo-server-uuid"),
        init_integration.entry_id,
    )
    database_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "demo-db-uuid"),
        init_integration.entry_id,
    )

    assert server_device is not None
    assert database_device is not None
    assert database_device.via_device_id == server_device.id


async def test_server_device_has_no_via_device(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """A server's own device is not linked via another device."""
    device_registry = dr.async_get(hass)
    server_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, "demo-server-uuid"),
        init_integration.entry_id,
    )

    assert server_device is not None
    assert server_device.via_device_id is None
