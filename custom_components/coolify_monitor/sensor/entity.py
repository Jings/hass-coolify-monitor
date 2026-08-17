"""Sensor entity for coolify_monitor."""

from collections.abc import Callable
from dataclasses import dataclass

from custom_components.coolify_monitor.coordinator import CoolifyMonitorCoordinatorData
from custom_components.coolify_monitor.entity import CoolifyMonitorEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class CoolifyMonitorSensorEntityDescription(SensorEntityDescription):
    """Describes a sensor and how to read it from coordinator data."""

    value_fn: Callable[[CoolifyMonitorCoordinatorData], StateType]


class CoolifyMonitorSensor(SensorEntity, CoolifyMonitorEntity):
    """Sensor backed by one value in the coordinator payload."""

    entity_description: CoolifyMonitorSensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the value read from coordinator data."""
        return self.entity_description.value_fn(self.coordinator.data)
