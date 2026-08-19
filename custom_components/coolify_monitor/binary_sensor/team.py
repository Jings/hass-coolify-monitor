"""Team binary sensor descriptions for coolify_monitor."""

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorTeamData
from homeassistant.const import EntityCategory

from .entity import CoolifyMonitorBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[CoolifyMonitorBinarySensorEntityDescription[CoolifyMonitorTeamData], ...] = (
    CoolifyMonitorBinarySensorEntityDescription(
        key="personal_team",
        translation_key="personal_team",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda team: team["personal_team"],
    ),
)
