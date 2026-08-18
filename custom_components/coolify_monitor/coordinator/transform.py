"""Transform raw Coolify API responses into the coordinator's data shape."""

from typing import Any

from .models import (
    CoolifyMonitorApplicationData,
    CoolifyMonitorCoordinatorData,
    CoolifyMonitorDatabaseData,
    CoolifyMonitorSelectedResources,
    CoolifyMonitorServerData,
)


def _split_status(status: str) -> tuple[str, str]:
    """
    Split Coolify's combined status field into state and health.

    Returns:
        The state (e.g. "running") and the health (e.g. "healthy"), or an
        empty health when the status carries no health suffix.

    """
    state, _, health = status.partition(":")
    return state, health


def _build_server(raw: dict[str, Any], version: str | None) -> CoolifyMonitorServerData:
    """
    Build a server entry from its raw API representation.

    Args:
        raw: The server's raw API representation.
        version: The Coolify instance's version, attached only to the host server.

    Returns:
        The server data the coordinator hands to entities.

    """
    return CoolifyMonitorServerData(
        uuid=raw["uuid"],
        name=raw["name"],
        description=raw["description"],
        is_reachable=raw["is_reachable"],
        is_usable=raw["is_usable"],
        is_coolify_host=raw["is_coolify_host"],
        coolify_version=version if raw["is_coolify_host"] else None,
    )


def _build_application(raw: dict[str, Any]) -> CoolifyMonitorApplicationData:
    """
    Build an application entry from its raw API representation.

    Returns:
        The application data the coordinator hands to entities.

    """
    state, health = _split_status(raw["status"])
    server = raw["destination"]["server"]
    return CoolifyMonitorApplicationData(
        uuid=raw["uuid"],
        name=raw["name"],
        description=raw["description"],
        state=state,
        health=health,
        fqdn=raw["fqdn"],
        git_repository=raw["git_repository"],
        git_branch=raw["git_branch"],
        server_uuid=server["uuid"],
        server_name=server["name"],
    )


def _build_database(raw: dict[str, Any]) -> CoolifyMonitorDatabaseData:
    """
    Build a database entry from its raw API representation.

    Returns:
        The database data the coordinator hands to entities.

    """
    state, health = _split_status(raw["status"])
    server = raw["destination"]["server"]
    return CoolifyMonitorDatabaseData(
        uuid=raw["uuid"],
        name=raw["name"],
        description=raw["description"],
        state=state,
        health=health,
        database_type=raw["database_type"],
        image=raw["image"],
        server_uuid=server["uuid"],
        server_name=server["name"],
    )


def build_coordinator_data(
    servers: list[dict[str, Any]],
    applications: list[dict[str, Any]],
    databases: list[dict[str, Any]],
    version: str | None = None,
) -> CoolifyMonitorCoordinatorData:
    """
    Combine the raw API responses into the coordinator's data shape.

    Args:
        servers: The raw server list.
        applications: The raw application list.
        databases: The raw database list.
        version: The Coolify instance's version, or None when it was not fetched.

    Returns:
        Every resource, grouped by kind and keyed by UUID.

    """
    return CoolifyMonitorCoordinatorData(
        servers={server["uuid"]: _build_server(server, version) for server in servers},
        applications={app["uuid"]: _build_application(app) for app in applications},
        databases={db["uuid"]: _build_database(db) for db in databases},
    )


def filter_to_selected(
    data: CoolifyMonitorCoordinatorData,
    selected: CoolifyMonitorSelectedResources,
) -> CoolifyMonitorCoordinatorData:
    """
    Narrow the coordinator's data down to only the resources the user chose to monitor.

    Returns:
        Every resource kind, keeping only the UUIDs present in `selected`.

    """
    return CoolifyMonitorCoordinatorData(
        servers={uuid: r for uuid, r in data["servers"].items() if uuid in selected["servers"]},
        applications={uuid: r for uuid, r in data["applications"].items() if uuid in selected["applications"]},
        databases={uuid: r for uuid, r in data["databases"].items() if uuid in selected["databases"]},
    )
