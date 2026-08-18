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


async def test_name_of_application(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the name of the application."""
    state = hass.states.get("sensor.demo_app_name")

    assert state is not None
    assert state.state == "demo-app"


async def test_description_of_application(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the description of the application."""
    state = hass.states.get("sensor.demo_app_description")

    assert state is not None
    assert state.state == "Demo application"


async def test_fqdn_of_application(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the application's URL."""
    state = hass.states.get("sensor.demo_app_url")

    assert state is not None
    assert state.state == "https://demo.example.com"


async def test_health_reflects_application_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the health half of the application's combined status."""
    state = hass.states.get("sensor.demo_app_health")

    assert state is not None
    assert state.state == "healthy"


async def test_server_name_of_application(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the name of the server the application runs on."""
    state = hass.states.get("sensor.demo_app_server")

    assert state is not None
    assert state.state == "localhost"
