"""Tests for the service sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_description_of_service(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the description of the service."""
    state = hass.states.get("sensor.service_demo_service_description")

    assert state is not None
    assert state.state == "Demo service"


async def test_service_type_of_service(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows which Coolify service template this is."""
    state = hass.states.get("sensor.service_demo_service_service_type")

    assert state is not None
    assert state.state == "it-tools"


async def test_health_reflects_service_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the health half of the service's combined status."""
    state = hass.states.get("sensor.service_demo_service_health")

    assert state is not None
    assert state.state == "healthy"


async def test_server_name_of_service(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the name of the server the service runs on."""
    state = hass.states.get("sensor.service_demo_service_server")

    assert state is not None
    assert state.state == "localhost"
