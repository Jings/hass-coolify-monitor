"""Constants for coolify_monitor."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "coolify_monitor"
ATTRIBUTION = "Data provided by your Coolify instance"

CONF_UPDATE_INTERVAL_MINUTES = "update_interval_minutes"
CONF_SELECTED_RESOURCES = "selected_resources"

DEFAULT_UPDATE_INTERVAL_MINUTES = 60
