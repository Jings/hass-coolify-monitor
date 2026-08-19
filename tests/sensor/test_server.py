"""Tests for the server sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_description_of_server(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the description of the server."""
    state = hass.states.get("sensor.server_localhost_description")

    assert state is not None
    assert state.state == "Demo server"


async def test_coolify_version_of_host_server(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the Coolify instance's version, since this server is the host."""
    state = hass.states.get("sensor.server_localhost_coolify_version")

    assert state is not None
    assert state.state == "4.0.0-beta.442"
