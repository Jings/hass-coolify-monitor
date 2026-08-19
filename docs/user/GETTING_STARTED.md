# Getting Started with Coolify Monitor

This guide will help you install and set up the Coolify Monitor custom integration for Home Assistant.

## Prerequisites

- Home Assistant 2025.7.0 or newer
- HACS (Home Assistant Community Store) installed
- Network connectivity from Home Assistant to your Coolify instance
- A Coolify API token (see below)

## Installation

### Via HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/Jings/hass-coolify-monitor`
6. Set category to "Integration"
7. Click "Add"
8. Find "Coolify Monitor" in the integration list
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/Jings/hass-coolify-monitor/releases)
2. Extract the `coolify_monitor` folder from the archive
3. Copy it to `custom_components/coolify_monitor/` in your Home Assistant configuration directory
4. Restart Home Assistant

## Create a Coolify API Token

In your Coolify instance, go to **Keys & Tokens** → **API tokens** and create a new token. Give it the
**Read Only** ability — this integration only ever reads data through Coolify's `/api/v1` endpoints; it
never deploys, restarts, or otherwise changes anything.

## Initial Setup

After installation, add the integration:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Coolify Monitor"
4. Follow the configuration steps:

### Step 1: Connection Information

Enter the required connection details:

- **Instance URL:** Your Coolify instance's address, including the scheme (e.g. `https://coolify.example.com`)
- **API token:** The Read Only token created above

Click **Submit** to test the connection. Home Assistant validates both the URL and the token by calling
Coolify's `/servers` endpoint.

### Step 2: Review Discovery

Home Assistant queries your Coolify instance for every server, application, database, team and service, and
shows a summary (e.g. "Found 1 server, 4 applications, 2 databases, 1 team and 1 service").

### Step 3: Choose What to Monitor

Pick which discovered resources you want entities for, grouped by category (Servers / Applications /
Databases / Teams / Services). Everything is preselected by default — deselect anything you don't need.

Click **Submit** to complete setup.

## What Gets Created

After successful setup, the integration creates one Home Assistant device per selected resource, for
example "Server: localhost" or "Application: recipe-app".

### Devices

Each device carries:

- A name prefixed with its resource kind (Server / Application / Database / Team / Service)
- `Coolify` as the manufacturer, and the resource kind as the model
- For applications, databases and services: a link back to the server device they run on

### Entities

The following entity kinds are created, depending on which resources you selected:

#### Sensors

- `sensor.<device_name>_description` — the resource's description, where Coolify provides one
- `sensor.<device_name>_health`, `..._database_type`, `..._service_type`, `..._server`, and other
  resource-specific details — see the main [README](../../README.md#available-entities) for the full list per
  resource kind

#### Binary Sensors

- `binary_sensor.<device_name>_connectivity` / `..._usable` — servers
- `binary_sensor.<device_name>_running` — applications, databases, services
- `binary_sensor.<device_name>_personal_team` — teams

## First Steps

### Dashboard Cards

Add entities to your dashboard:

1. Go to your dashboard
2. Click **Edit Dashboard** → **Add Card**
3. Choose card type (e.g., "Entities", "Glance")
4. Select entities from "Coolify Monitor"

Example entities card for one application:

```yaml
type: entities
title: recipe-app
entities:
  - binary_sensor.application_recipe_app_running
  - sensor.application_recipe_app_health
  - sensor.application_recipe_app_url
```

### Automations

Use the integration in automations:

**Example — notify when an application stops running:**

```yaml
automation:
  - alias: "Alert when recipe-app stops"
    trigger:
      - trigger: state
        entity_id: binary_sensor.application_recipe_app_running
        to: "off"
        for:
          minutes: 5
    action:
      - action: notify.notify
        data:
          message: "recipe-app is no longer running"
```

**Example — refresh data on a schedule:**

```yaml
automation:
  - alias: "Refresh Coolify data every morning"
    trigger:
      - trigger: time
        at: "07:00:00"
    action:
      - action: coolify_monitor.refresh_data
        data:
          config_entry_id: 01JG3T2Q6Z9K4V8P0N5R7X2M1A
```

## Troubleshooting

### Connection Failed

If setup fails with "Unable to connect to the Coolify instance":

1. Verify the instance URL is correct and reachable from Home Assistant
2. Check that the Coolify instance itself is running
3. Check Home Assistant logs for detailed error messages

### Invalid Token

If setup fails with "The API token is invalid or has been revoked":

1. Verify the token was copied correctly
2. Check the token wasn't revoked in Coolify under Keys & Tokens

### Entities Not Updating

If entities show "Unavailable" or don't update:

1. Check that the Coolify instance is online and reachable
2. Verify the API token hasn't expired or been revoked — Home Assistant should prompt for reauthentication
   automatically if it has
3. Review logs: **Settings** → **System** → **Logs**
4. Try reloading the integration, or call the `coolify_monitor.refresh_data` service action

### Debug Logging

Enable debug logging to troubleshoot issues:

```yaml
logger:
  default: warning
  logs:
    custom_components.coolify_monitor: debug
```

Add this to `configuration.yaml`, restart, and reproduce the issue. Check logs for detailed information.

## Next Steps

- See [CONFIGURATION.md](./CONFIGURATION.md) for detailed configuration options
- See [EXAMPLES.md](./EXAMPLES.md) for more automation examples
- Report issues at [GitHub Issues](https://github.com/Jings/hass-coolify-monitor/issues)

## Support

For help and discussion:

- [GitHub Discussions](https://github.com/Jings/hass-coolify-monitor/discussions)
- [Home Assistant Community Forum](https://community.home-assistant.io/)
