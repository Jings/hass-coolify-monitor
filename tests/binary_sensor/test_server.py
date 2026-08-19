"""Tests for the server binary sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant


async def test_reachable_reflects_server_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The connectivity sensor is on when the server reports itself reachable."""
    state = hass.states.get("binary_sensor.server_localhost_connectivity")

    assert state is not None
    assert state.state == STATE_ON


async def test_usable_reflects_server_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The usable sensor is on when the server reports itself usable."""
    state = hass.states.get("binary_sensor.server_localhost_usable")

    assert state is not None
    assert state.state == STATE_ON
