"""
API package for coolify_monitor.

Exception hierarchy:
    CoolifyMonitorApiClientError (base)
    ├── CoolifyMonitorApiClientCommunicationError (network/timeout)
    └── CoolifyMonitorApiClientAuthenticationError (401/403)

The coordinator maps them onto ConfigEntryAuthFailed and UpdateFailed; nothing else
in the integration imports this package.
"""

from .client import (
    FAN_SPEEDS,
    CoolifyMonitorApiClient,
    CoolifyMonitorApiClientAuthenticationError,
    CoolifyMonitorApiClientCommunicationError,
    CoolifyMonitorApiClientError,
)

__all__ = [
    "FAN_SPEEDS",
    "CoolifyMonitorApiClient",
    "CoolifyMonitorApiClientAuthenticationError",
    "CoolifyMonitorApiClientCommunicationError",
    "CoolifyMonitorApiClientError",
]
