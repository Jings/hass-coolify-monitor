# Configuration Reference

This document describes all configuration options and settings available in the Coolify Monitor custom integration.

## Integration Configuration

### Initial Setup Options

These options are configured during initial setup via the Home Assistant UI.

#### Connection Settings

| Option           | Type   | Required | Default | Description                                                           |
| ---------------- | ------ | -------- | ------- | --------------------------------------------------------------------- |
| **Instance URL** | string | Yes      | -       | Your Coolify instance's address, including the scheme (http or https) |
| **API token**    | string | Yes      | -       | A Read Only API token, created in Coolify under Keys & Tokens         |

Both are validated together by calling Coolify's `/servers` endpoint — a successful response proves the URL
and token both work.

#### Resource Selection

After the connection is validated, Home Assistant auto-discovers every server, application, database, team
and service on the instance and lets you choose which ones get entities, grouped by category. Everything is
preselected by default.

### Options Flow (Reconfiguration)

After initial setup, you can modify settings:

1. Go to **Settings** → **Devices & Services**
2. Find "Coolify Monitor"
3. Click **Configure**
4. Choose **Update interval** or **Resources**
5. Modify settings, then click **Submit**

**Available options:**

- **Update interval** — how often to poll Coolify, in minutes (1–1440, default 60)
- **Resources** — re-runs discovery (so newly added Coolify resources become selectable) and lets you change
  which resources are monitored

Changing the instance URL or API token itself is a **Reconfigure**, not an option — see
[Troubleshooting → Manual Credential Update](../../README.md#manual-credential-update) in the main README.

## Entity Configuration

### Entity Customization

Customize entities via the UI or `configuration.yaml`:

#### Via Home Assistant UI

1. Go to **Settings** → **Devices & Services** → **Entities**
2. Find and click the entity
3. Click the settings icon
4. Modify:
   - Entity ID
   - Name
   - Icon
   - Area assignment

#### Via configuration.yaml

```yaml
homeassistant:
  customize:
    sensor.application_recipe_app_health:
      friendly_name: "recipe-app health"
```

### Disabling Entities

If you don't need certain entities:

1. Go to **Settings** → **Devices & Services** → **Entities**
2. Find the entity
3. Click it, then click **Settings** icon
4. Toggle **Enable entity** off

Disabled entities won't update or consume resources. To stop monitoring an entire resource instead, deselect
it in the options flow's **Resources** step — see above.

## Services

The integration provides the following service action:

### `coolify_monitor.refresh_data`

Fetch the current Coolify state immediately instead of waiting for the next poll.

**Service data:**

| Parameter         | Type   | Required | Description                        |
| ----------------- | ------ | -------- | ---------------------------------- |
| `config_entry_id` | string | Yes      | The configuration entry to refresh |

The action returns `refreshed_at`, `success` and `value_count`, so an automation can react to
whether the refresh actually produced data.

**Example:**

```yaml
action: coolify_monitor.refresh_data
data:
  config_entry_id: 01JG3T2Q6Z9K4V8P0N5R7X2M1A
```

### Using Services in Automations

```yaml
automation:
  - alias: "Refresh at sunset"
    trigger:
      - trigger: sun
        event: sunset
    action:
      - action: coolify_monitor.refresh_data
        data:
          config_entry_id: 01JG3T2Q6Z9K4V8P0N5R7X2M1A
```

## Advanced Configuration

### Multiple Instances

You can add multiple instances of this integration for different Coolify instances:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Coolify Monitor"
4. Configure with a different instance URL and token

Each instance creates separate devices and entities with unique entity IDs. Pointing a second entry at the
same instance is rejected — the discovered server's unique ID is compared against every existing entry.

### Polling Behavior

The integration polls Coolify's REST API on a fixed interval:

- **Minimum interval:** 1 minute
- **Maximum interval:** 1440 minutes (24 hours)
- **Default interval:** 60 minutes

Coolify's own API defaults to a 200 requests/minute rate limit; stay well under that, especially with a short
interval on an instance with many resources selected.

Adjust based on your needs:

- Frequent status checks: 1–5 minutes
- Regular monitoring: 60 minutes (default)
- Slow-changing values (teams, rarely-deployed apps): several hours

## Diagnostic Data

The integration provides diagnostic data for troubleshooting:

1. Go to **Settings** → **Devices & Services**
2. Find "Coolify Monitor"
3. Click on the device
4. Click **Download Diagnostics**

Diagnostic data includes:

- Config entry state and version
- Coordinator update status and last error, if any
- The current coordinator data for every monitored resource

**Privacy note:** The API token is always redacted from diagnostic downloads. Review the rest before sharing,
since it includes your Coolify resource names and URLs.

## Configuration Examples

See [EXAMPLES.md](./EXAMPLES.md) for complete automation and dashboard examples.

## Troubleshooting Configuration

### Config Entry Fails to Load

If the integration fails to load after configuration:

1. Check Home Assistant logs for errors
2. Verify the instance URL and API token are still correct
3. Test connectivity from Home Assistant to the Coolify instance
4. Try removing and re-adding the integration

### Options Don't Save

If configuration changes aren't persisted:

1. Check for validation errors in the UI
2. Ensure the update interval is within 1–1440 minutes
3. Review logs for detailed error messages
4. Try restarting Home Assistant

## Related Documentation

- [Getting Started](./GETTING_STARTED.md) - Installation and initial setup
- [Examples](./EXAMPLES.md) - Automation and dashboard examples
- [GitHub Issues](https://github.com/Jings/hass-coolify-monitor/issues) - Report problems
