"""Service sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorServiceData
from homeassistant.const import EntityCategory

from .entity import CoolifyMonitorSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorSensorEntityDescription[CoolifyMonitorServiceData], ...] = (
    CoolifyMonitorSensorEntityDescription(
        key="description",
        translation_key="description",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda service: service["description"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="service_type",
        translation_key="service_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda service: service["service_type"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="health",
        translation_key="health",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda service: service["health"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="server_name",
        translation_key="server_name",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda service: service["server_name"],
    ),
)
