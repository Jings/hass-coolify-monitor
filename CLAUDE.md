# Home Assistant Custom Integration: Coolify Monitor

## Goal

A custom component for Home Assistant that monitors a self-hosted Coolify
instance: servers, applications, services and databases are auto-discovered
and exposed as entities. The user only provides the instance URL and an API
token; afterwards they use the options flow to choose which resources they
want as entities/dashboard cards.

Data source: the official, documented Coolify REST API (`/api/v1`) — no
scraping, no legal grey area.

## Tech stack

- Python 3.14+, Home Assistant custom integration architecture (see
  `AGENTS.md` for the enforced package layout and coding rules)
- `DataUpdateCoordinator` for centralized polling (one coordinator per
  Coolify instance, feeding all entities)
- A multi-step config flow: 1) connection details, 2) show the
  auto-discovery result, 3) select which resources to monitor
- `voluptuous` for schema validation
- HTTP client: `aiohttp` (already part of HA core, no extra requirement)

## Identity

- **Domain:** `coolify_monitor`
- **Class prefix:** `CoolifyMonitor`
- **Repository:** Jings/hass-coolify-monitor

This matches what `initialize.sh` already set up across `manifest.json`,
`const.py` and `AGENTS.md` — use it everywhere, never the shorter `coolify`
variant from earlier drafts of this plan.

## Authentication

- Bearer token auth (Laravel Sanctum), no OAuth
- The user creates the token themselves in the Coolify UI under
  "Keys & Tokens" → "API tokens"
- The token is collected in the config flow as a password field
  (`vol.Required` with `selector.TextSelector(TextSelectorConfig(type="password"))`)
- Documentation should recommend creating the token with the "Read Only"
  ability, since the integration only reads (no deploy/restart in v1)
- Respect the rate limit: Coolify defaults to 200 requests/minute — stay
  well under that when polling (see update interval below)
- The token is stored via `entry.data`; non-sensitive selection data (which
  resources to monitor) goes in `entry.options` instead — see
  `.agents/instructions/blueprint.config_flow.instructions.md` for the
  data-vs-options split this project enforces

## Where the code lives

Package layout, naming and the three-layer architecture (entities →
coordinator → API client) are fixed by `AGENTS.md` § Integration Structure —
this plan does not repeat them. In short: the real API client goes in
`api/`, the coordinator in `coordinator/`, the config/options flow in
`config_flow_handler/`, and each entity platform gets its own package
(`sensor/`, `binary_sensor/`, …) with one entity class per file.

## Step-by-step plan

### 1. API layer (`api/client.py`)

- A thin async client around the relevant endpoints:
  - `GET /api/v1/servers` — server list incl. status; also doubles as the
    config flow's connection test, since the entry it doesn't have to search
    for (`is_coolify_host: true`) gives us a stable per-instance unique ID
    for free, in the same call
  - `GET /api/v1/applications` — applications incl. status, last deploy
  - `GET /api/v1/databases` — database resources
  - `GET /api/v1/services` — services (e.g. Immich, Home Assistant itself) —
    deferred until a real payload can be captured (see the services section
    of this plan)
- Own exception hierarchy: `CoolifyMonitorApiClientCommunicationError`
  (network/timeout), `CoolifyMonitorApiClientAuthenticationError` (401/403 →
  wrong or expired token) — see `blueprint.coordinator.instructions.md` for
  the required shape
- Type all responses (`dataclasses` or `TypedDict`) so discovery and the
  coordinator/entities use the same structure
- Timeout generous enough for VPS instances with many resources (e.g. 15s)

### 2. Config flow — step 1: connection (`config_flow_handler/config_flow.py`)

- Form: `url` (instance URL, e.g. `https://coolify.example.com`),
  `api_token` (password field)
- Validate by calling `/api/v1/servers`: a successful response proves the URL
  and token both work, and its `is_coolify_host: true` entry supplies the
  unique ID — no separate `/version` call needed
- Separate error keys: `cannot_connect` (URL wrong/unreachable) vs.
  `invalid_auth` (token wrong)
- Reconfigure and reauth re-run the same validation and compare the
  discovered unique ID against the entry's existing one
  (`_abort_if_unique_id_mismatch()`), so pointing the form at a different
  Coolify instance aborts instead of silently adopting it

### 3. Config flow — step 2: auto-discovery

- After a successful connection: query all four endpoints (`servers`,
  `applications`, `databases`, `services`) concurrently (`asyncio.gather`)
- Don't just wave the result through — summarize it in an intermediate step
  (e.g. "Found: 1 server, 4 applications, 2 databases, 1 service") to build
  confidence that discovery actually worked

### 4. Config flow — step 3: resource selection

- Multi-select form (`selector.SelectSelector` with `multiple: true`),
  grouped by category (Server / Applications / Databases / Services),
  pre-selected with "everything selected" as a sensible default
- Selected UUIDs are stored in `entry.options["selected_resources"]`
  (this is user-tunable behavior, not connection identity — see the
  data-vs-options split above)
- The **options flow** replicates this exact selection step, including a
  fresh discovery run (in case new apps were added since initial setup) —
  so the user can adjust at any time without re-adding the integration

### 5. Coordinator (`coordinator/base.py`)

- One coordinator per config entry, `update_interval` configurable via
  `entry.options` (default e.g. 60s — Coolify metrics change faster than
  once a day, but keep the 200 req/min limit in mind, see the rate-limit
  note above)
- `_async_update_data()`: fetches only the resources the user selected (no
  unnecessary traffic for deselected items), aggregates into a dict keyed by
  resource UUID
- Raise `UpdateFailed` on connection errors; raise `ConfigEntryAuthFailed`
  when the API reports invalid credentials, so Home Assistant triggers the
  reauth flow if the token expired or was revoked

### 6. Entities

- **`entity/base.py`**: `CoolifyMonitorEntity(CoordinatorEntity)` as the
  base class, reads its own resource by UUID from `coordinator.data`, sets
  `device_info` (one HA "device" per Coolify resource, so entities group
  cleanly, e.g. "App: recipe-app")
- **`binary_sensor/`**: running/stopped/degraded status per server,
  application, database, service
- **`sensor/`**:
  - Applications: status text, last deployment timestamp, deployment result
    (success/failed)
  - Server: CPU/RAM usage (if the API provides it), number of running
    containers
  - Databases/services: status, version if available
- Entities are created dynamically only for selected resources
  (`async_setup_entry` iterates over `entry.options["selected_resources"]`)

### 7. Dashboard aspect ("show it on the dashboard")

- For v1: no custom Lovelace card — instead make the device grouping (step 6) clean enough that HA's auto-generated dashboard produces usable cards
  per resource out of the box
- Optional for later: a custom Lovelace strategy element, or docs with
  example dashboard YAML (not required for the first version)

### 8. Testing

- Test against a real Coolify instance: run through the config flow, check
  that discovery finds all current apps/services
- Failure cases: wrong token, instance offline, token revoked afterwards in
  Coolify (the reauth flow should kick in)
- Check that newly added Coolify apps become selectable afterwards via the
  options-flow discovery

### 9. Optional (later, not needed for v1)

- Action entities to restart/redeploy an application directly from HA
  (requires a token with `write`/`deploy` ability — a deliberate decision,
  since that carries more risk than read-only)
- Diagnostics support for debug export (token redacted — required either
  way per `AGENTS.md`)
- HACS publication once v1 is stable — no legal hurdles here, just code
  quality/docs

## Open questions to settle before starting

- Which fields does `/api/v1/servers` actually return for CPU/RAM usage?
  (Check against the API reference — this data may not be available at all
  without Coolify's separate "Sentinel" agent for server metrics)
- Test the token permission levels on your actual Coolify version (older
  versions reportedly only had "Read Only" vs. "\*" without finer-grained
  scopes — relevant for the documentation recommendation to users)
- `manifest.json` currently sets `iot_class: cloud_polling` from the
  initializer's default. Decide deliberately: `local_polling` fits a
  self-hosted instance reached over the LAN, `cloud_polling` fits one
  reached only through a public URL. See
  `.agents/instructions/blueprint.manifest.instructions.md`.
