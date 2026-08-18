"""
Entity package for coolify_monitor.

Architecture:
    All platform entities inherit from (PlatformEntity, CoolifyMonitorEntity).
    MRO order matters — platform-specific class first, then the integration base.
    Entities read data from coordinator.data and NEVER call the API client directly.
    Unique IDs follow the pattern: {resource_uuid}_{description.key}

See entity/base.py for the CoolifyMonitorEntity base class.
"""

from .base import CoolifyMonitorEntity

__all__ = ["CoolifyMonitorEntity"]
