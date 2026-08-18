"""Application sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorApplicationData
from homeassistant.const import EntityCategory

from .entity import CoolifyMonitorSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorSensorEntityDescription[CoolifyMonitorApplicationData], ...] = (
    CoolifyMonitorSensorEntityDescription(
        key="git_branch",
        translation_key="git_branch",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda application: application["git_branch"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="name",
        translation_key="name",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda application: application["name"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="description",
        translation_key="description",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda application: application["description"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="fqdn",
        translation_key="fqdn",
        value_fn=lambda application: application["fqdn"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="health",
        translation_key="health",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda application: application["health"],
    ),
    CoolifyMonitorSensorEntityDescription(
        key="server_name",
        translation_key="server_name",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda application: application["server_name"],
    ),
)
