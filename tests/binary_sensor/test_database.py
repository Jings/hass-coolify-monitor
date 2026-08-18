"""Tests for the database binary sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant


async def test_running_reflects_database_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The running sensor is on when the database state is running."""
    state = hass.states.get("binary_sensor.demo_db_running")

    assert state is not None
    assert state.state == STATE_ON
