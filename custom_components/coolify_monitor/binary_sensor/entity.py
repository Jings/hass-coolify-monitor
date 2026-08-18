"""Binary sensor entity for coolify_monitor."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorServerData
from custom_components.coolify_monitor.entity import CoolifyMonitorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription


@dataclass(frozen=True, kw_only=True)
class CoolifyMonitorBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a binary sensor and how to read it from a server's data."""

    value_fn: Callable[[CoolifyMonitorServerData], bool | None]


class CoolifyMonitorBinarySensor(BinarySensorEntity, CoolifyMonitorEntity):
    """Binary sensor backed by one value in its own server's data."""

    entity_description: CoolifyMonitorBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return the value read from this entity's own resource."""
        resource = self.coordinator.data[self.resource_kind][self.resource_uuid]
        return self.entity_description.value_fn(cast("CoolifyMonitorServerData", resource))
