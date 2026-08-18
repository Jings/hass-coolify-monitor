"""Database sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorDatabaseData
from homeassistant.const import EntityCategory

from .entity import CoolifyMonitorSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorSensorEntityDescription[CoolifyMonitorDatabaseData], ...] = (
    CoolifyMonitorSensorEntityDescription(
        key="description",
        translation_key="description",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda database: database["description"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="database_type",
        translation_key="database_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda database: database["database_type"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="image",
        translation_key="image",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda database: database["image"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="health",
        translation_key="health",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda database: database["health"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="server_name",
        translation_key="server_name",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda database: database["server_name"],
    ),
)
