"""Application binary sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorApplicationData
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .entity import CoolifyMonitorBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorBinarySensorEntityDescription[CoolifyMonitorApplicationData], ...] = (
    CoolifyMonitorBinarySensorEntityDescription(
        key="running",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda application: application["state"] == "running",
    ),
)
