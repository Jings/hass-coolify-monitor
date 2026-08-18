"""Server binary sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorServerData
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .entity import CoolifyMonitorBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorBinarySensorEntityDescription[CoolifyMonitorServerData], ...] = (
    CoolifyMonitorBinarySensorEntityDescription(
        key="reachable",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda server: server["is_reachable"],
    ),
)
