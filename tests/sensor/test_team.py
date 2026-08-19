"""Tests for the team sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_description_of_team(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the description of the team, or unknown when Coolify reports none."""
    state = hass.states.get("sensor.team_root_team_description")

    assert state is not None
    assert state.state == "unknown"


async def test_created_at_of_team(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows when the team was created."""
    state = hass.states.get("sensor.team_root_team_timestamp")

    assert state is not None
    assert state.state == "2025-09-03T18:18:38+00:00"
