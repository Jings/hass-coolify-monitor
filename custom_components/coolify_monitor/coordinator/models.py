"""Typed shapes for the data the coordinator hands to entities."""

from typing import Literal, TypedDict

CoolifyMonitorResourceKind = Literal["servers", "applications", "databases"]


class CoolifyMonitorServerData(TypedDict):
    """One Coolify server, as the coordinator exposes it to entities."""

    uuid: str
    name: str
    description: str
    is_reachable: bool
    is_usable: bool
    is_coolify_host: bool
    coolify_version: str | None


class CoolifyMonitorApplicationData(TypedDict):
    """One Coolify application, as the coordinator exposes it to entities."""

    uuid: str
    name: str
    description: str
    state: str
    health: str
    fqdn: str
    git_repository: str
    git_branch: str
    server_uuid: str
    server_name: str


class CoolifyMonitorDatabaseData(TypedDict):
    """One Coolify database, as the coordinator exposes it to entities."""

    uuid: str
    name: str
    description: str
    state: str
    health: str
    database_type: str
    image: str
    server_uuid: str
    server_name: str


class CoolifyMonitorCoordinatorData(TypedDict):
    """Every Coolify resource the coordinator has fetched, grouped by kind and keyed by UUID."""

    servers: dict[str, CoolifyMonitorServerData]
    applications: dict[str, CoolifyMonitorApplicationData]
    databases: dict[str, CoolifyMonitorDatabaseData]


class CoolifyMonitorSelectedResources(TypedDict):
    """Which discovered UUIDs the user chose to monitor, grouped by kind."""

    servers: list[str]
    applications: list[str]
    databases: list[str]
