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
)
