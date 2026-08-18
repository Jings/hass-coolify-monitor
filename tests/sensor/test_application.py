"""Tests for the application sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_git_branch_reflects_deployed_branch(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the deployed branch."""
    state = hass.states.get("sensor.demo_app_git_branch")

    assert state is not None
    assert state.state == "main"
