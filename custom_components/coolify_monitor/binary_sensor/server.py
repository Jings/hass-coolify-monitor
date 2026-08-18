"""Server binary sensor descriptions for coolify_monitor."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .entity import CoolifyMonitorBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorBinarySensorEntityDescription, ...] = (
    CoolifyMonitorBinarySensorEntityDescription(
        key="reachable",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda server: server["is_reachable"],
    ),
)
