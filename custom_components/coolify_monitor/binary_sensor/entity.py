"""Binary sensor entity for coolify_monitor."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from custom_components.coolify_monitor.entity import CoolifyMonitorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription


@dataclass(frozen=True, kw_only=True)
class CoolifyMonitorBinarySensorEntityDescription[ResourceT](BinarySensorEntityDescription):
    """Describes a binary sensor and how to read it from its own resource's data."""

    value_fn: Callable[[ResourceT], bool | None]


class CoolifyMonitorBinarySensor[ResourceT](BinarySensorEntity, CoolifyMonitorEntity):
    """Binary sensor backed by one value in its own resource's data."""

    entity_description: CoolifyMonitorBinarySensorEntityDescription[ResourceT]

    @property
    def is_on(self) -> bool | None:
        """Return the value read from this entity's own resource."""
        resource = self.coordinator.data[self.resource_kind][self.resource_uuid]
        return self.entity_description.value_fn(cast(ResourceT, resource))
