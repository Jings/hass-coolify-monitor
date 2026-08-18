"""Server sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorServerData
from homeassistant.const import EntityCategory

from .entity import CoolifyMonitorSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorSensorEntityDescription[CoolifyMonitorServerData], ...] = (
    CoolifyMonitorSensorEntityDescription(
        key="description",
        translation_key="description",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda server: server["description"],
    ),
)
