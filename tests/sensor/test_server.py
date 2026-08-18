"""Tests for the server sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_description_of_server(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the description of the server."""
    state = hass.states.get("sensor.localhost_description")

    assert state is not None
    assert state.state == "Demo server"
