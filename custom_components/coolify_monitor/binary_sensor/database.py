"""Database binary sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorDatabaseData
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .entity import CoolifyMonitorBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorBinarySensorEntityDescription[CoolifyMonitorDatabaseData], ...] = (
    CoolifyMonitorBinarySensorEntityDescription(
        key="running",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda database: database["state"] == "running",
    ),
)
