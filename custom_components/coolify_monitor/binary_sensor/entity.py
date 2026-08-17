"""Binary sensor entity for coolify_monitor."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.coolify_monitor.entity import CoolifyMonitorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription


@dataclass(frozen=True, kw_only=True)
class CoolifyMonitorBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a binary sensor and how to read it from coordinator data."""

    value_fn: Callable[[dict[str, Any]], bool | None]


class CoolifyMonitorBinarySensor(BinarySensorEntity, CoolifyMonitorEntity):
    """Binary sensor backed by one value in the coordinator payload."""

    entity_description: CoolifyMonitorBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return the value read from coordinator data."""
        return self.entity_description.value_fn(self.coordinator.data)
