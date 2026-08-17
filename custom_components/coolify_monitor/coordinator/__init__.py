"""Data update coordinator package for coolify_monitor."""

from .base import CoolifyMonitorDataUpdateCoordinator
from .models import CoolifyMonitorCoordinatorData

__all__ = ["CoolifyMonitorCoordinatorData", "CoolifyMonitorDataUpdateCoordinator"]
