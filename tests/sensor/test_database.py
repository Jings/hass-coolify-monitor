"""Tests for the database sensor descriptions."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_description_of_database(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the description of the database."""
    state = hass.states.get("sensor.demo_db_description")

    assert state is not None
    assert state.state == "Demo database"


async def test_database_type_of_database(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows which kind of database this is."""
    state = hass.states.get("sensor.demo_db_database_type")

    assert state is not None
    assert state.state == "standalone-postgresql"


async def test_image_of_database(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the database's container image, standing in for a version."""
    state = hass.states.get("sensor.demo_db_image")

    assert state is not None
    assert state.state == "postgres:17-alpine"


async def test_health_reflects_database_status(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the health half of the database's combined status."""
    state = hass.states.get("sensor.demo_db_health")

    assert state is not None
    assert state.state == "healthy"


async def test_server_name_of_database(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """The sensor shows the name of the server the database runs on."""
    state = hass.states.get("sensor.demo_db_server")

    assert state is not None
    assert state.state == "localhost"
