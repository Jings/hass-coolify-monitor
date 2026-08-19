"""Tests for the team binary sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant


async def test_personal_team_reflects_team_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The personal team sensor is on when the team is a personal team."""
    state = hass.states.get("binary_sensor.team_root_team_personal_team")

    assert state is not None
    assert state.state == STATE_ON
