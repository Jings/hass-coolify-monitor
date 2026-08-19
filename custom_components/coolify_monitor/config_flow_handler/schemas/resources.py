"""Schema for selecting which discovered resources to monitor."""

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.coolify_monitor.coordinator import CoolifyMonitorCoordinatorData
from custom_components.coolify_monitor.coordinator.models import CoolifyMonitorSelectedResources
from homeassistant.helpers import selector

FIELD_SELECTED_SERVERS = "selected_servers"
FIELD_SELECTED_APPLICATIONS = "selected_applications"
FIELD_SELECTED_DATABASES = "selected_databases"
FIELD_SELECTED_TEAMS = "selected_teams"
FIELD_SELECTED_SERVICES = "selected_services"


def _options_for(resources: Mapping[str, Any]) -> list[selector.SelectOptionDict]:
    """
    Build the selectable options for one resource category.

    Returns:
        One option per discovered resource, labeled with its name.

    """
    return [selector.SelectOptionDict(value=uuid, label=resource["name"]) for uuid, resource in resources.items()]


def _default_for(resources: Mapping[str, Any], selected: list[str] | None) -> list[str]:
    """
    Pick which UUIDs of one resource category should start preselected.

    Returns:
        Every discovered UUID when nothing was selected before, otherwise only
        the ones that are both discovered and previously selected.

    """
    if selected is None:
        return list(resources)
    selected_set = set(selected)
    return [uuid for uuid in resources if uuid in selected_set]


def get_resources_schema(
    discovered: CoolifyMonitorCoordinatorData,
    selected: CoolifyMonitorSelectedResources | None = None,
) -> vol.Schema:
    """
    Build the schema for choosing which discovered resources to monitor.

    Args:
        discovered: Every resource found on the Coolify instance, grouped by kind.
        selected: The UUIDs to preselect per kind, or None to preselect everything.

    Returns:
        The voluptuous schema for the resource-selection form.

    """
    return vol.Schema(
        {
            vol.Optional(
                FIELD_SELECTED_SERVERS,
                default=_default_for(discovered["servers"], selected["servers"] if selected else None),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_options_for(discovered["servers"]),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                ),
            ),
            vol.Optional(
                FIELD_SELECTED_APPLICATIONS,
                default=_default_for(
                    discovered["applications"],
                    selected["applications"] if selected else None,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_options_for(discovered["applications"]),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                ),
            ),
            vol.Optional(
                FIELD_SELECTED_DATABASES,
                default=_default_for(discovered["databases"], selected["databases"] if selected else None),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_options_for(discovered["databases"]),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                ),
            ),
            vol.Optional(
                FIELD_SELECTED_TEAMS,
                default=_default_for(discovered["teams"], selected["teams"] if selected else None),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_options_for(discovered["teams"]),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                ),
            ),
            vol.Optional(
                FIELD_SELECTED_SERVICES,
                default=_default_for(discovered["services"], selected["services"] if selected else None),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_options_for(discovered["services"]),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                ),
            ),
        },
    )


def build_selected_resources(user_input: Mapping[str, Any]) -> CoolifyMonitorSelectedResources:
    """
    Turn the three submitted selections into the coordinator's selection shape.

    Returns:
        The selected UUIDs, grouped by resource kind.

    """
    return CoolifyMonitorSelectedResources(
        servers=user_input[FIELD_SELECTED_SERVERS],
        applications=user_input[FIELD_SELECTED_APPLICATIONS],
        databases=user_input[FIELD_SELECTED_DATABASES],
        teams=user_input[FIELD_SELECTED_TEAMS],
        services=user_input[FIELD_SELECTED_SERVICES],
    )


__all__ = [
    "build_selected_resources",
    "get_resources_schema",
]
