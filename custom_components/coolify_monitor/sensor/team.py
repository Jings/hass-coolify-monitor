"""Team sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorTeamData
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory

from .entity import CoolifyMonitorSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorSensorEntityDescription[CoolifyMonitorTeamData], ...] = (
    CoolifyMonitorSensorEntityDescription(
        key="description",
        translation_key="description",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda team: team["description"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="created_at",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda team: team["created_at"],
    ),
)
