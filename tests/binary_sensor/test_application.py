"""Tests for the application binary sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant


async def test_running_reflects_application_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The running sensor is on when the application state is running."""
    state = hass.states.get("binary_sensor.application_demo_app_running")

    assert state is not None
    assert state.state == STATE_ON
