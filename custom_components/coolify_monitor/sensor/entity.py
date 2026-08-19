"""Sensor entity for coolify_monitor."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import cast

from custom_components.coolify_monitor.entity import CoolifyMonitorEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType

type _SensorValue = StateType | date | datetime | Decimal


@dataclass(frozen=True, kw_only=True)
class CoolifyMonitorSensorEntityDescription[ResourceT](SensorEntityDescription):
    """Describes a sensor and how to read it from its own resource's data."""

    value_fn: Callable[[ResourceT], _SensorValue]


class CoolifyMonitorSensor[ResourceT](SensorEntity, CoolifyMonitorEntity):
    """Sensor backed by one value in its own resource's data."""

    entity_description: CoolifyMonitorSensorEntityDescription[ResourceT]

    @property
    def native_value(self) -> _SensorValue:
        """Return the value read from this entity's own resource."""
        resource = self.coordinator.data[self.resource_kind][self.resource_uuid]
        return self.entity_description.value_fn(cast(ResourceT, resource))
