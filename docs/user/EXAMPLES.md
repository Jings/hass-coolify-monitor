# Examples

This page provides ready-to-use examples for automations and dashboards with the Coolify Monitor custom
integration.

Replace entity IDs like `binary_sensor.application_recipe_app_running` with your actual entity IDs after
setting up the integration — they follow the pattern `<platform>.<resource_kind>_<resource_name>_<detail>`.

## Automations

### Notify when an application stops running

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
          title: "Application down"
          message: "recipe-app is no longer running on Coolify"
```

### Notify when a server becomes unreachable

```yaml
automation:
  - alias: "Alert on server connectivity loss"
    trigger:
      - trigger: state
        entity_id: binary_sensor.server_localhost_connectivity
        to: "off"
        for:
          minutes: 5
    action:
      - action: notify.notify
        data:
          title: "Server unreachable"
          message: "Coolify can no longer reach this server"
```

### Notify when a database's health degrades

```yaml
automation:
  - alias: "Alert on unhealthy database"
    trigger:
      - trigger: state
        entity_id: sensor.database_demo_db_health
        to: "unhealthy"
    action:
      - action: notify.notify
        data:
          title: "Database unhealthy"
          message: "demo-db reported an unhealthy status"
```

### Call the refresh service on a schedule

```yaml
automation:
  - alias: "Refresh Coolify data every morning"
    trigger:
      - trigger: time
        at: "03:00:00"
    action:
      - action: coolify_monitor.refresh_data
        data:
          config_entry_id: 01JG3T2Q6Z9K4V8P0N5R7X2M1A
```

### Use a blueprint for status alerts

Save this as a blueprint file and import it in Home Assistant:

```yaml
blueprint:
  name: Coolify Monitor — Resource Down Alert
  description: Send a notification when a monitored resource stops running.
  domain: automation
  input:
    running_entity:
      name: Running binary sensor
      selector:
        entity:
          domain: binary_sensor
          integration: coolify_monitor
    notify_target:
      name: Notification service
      default: notify.notify
      selector:
        text:

trigger:
  - trigger: state
    entity_id: !input running_entity
    to: "off"
    for:
      minutes: 5

action:
  - action: !input notify_target
    data:
      message: >-
        {{ state_attr(trigger.entity_id, 'friendly_name') }} stopped running.
```

## Dashboard Cards

### Application summary — entities card

```yaml
type: entities
title: recipe-app
entities:
  - entity: binary_sensor.application_recipe_app_running
    name: Running
  - entity: sensor.application_recipe_app_health
    name: Health
  - entity: sensor.application_recipe_app_url
    name: URL
  - entity: sensor.application_recipe_app_server
    name: Server
```

### Server status — glance card

```yaml
type: glance
title: Coolify Server
entities:
  - entity: binary_sensor.server_localhost_connectivity
    name: Reachable
  - entity: binary_sensor.server_localhost_usable
    name: Usable
  - entity: sensor.server_localhost_coolify_version
    name: Version
show_state: true
```

### Database summary — entities card

```yaml
type: entities
title: demo-db
entities:
  - entity: binary_sensor.database_demo_db_running
    name: Running
  - entity: sensor.database_demo_db_health
    name: Health
  - entity: sensor.database_demo_db_database_type
    name: Type
  - entity: sensor.database_demo_db_image
    name: Image
```

## Related Documentation

- [Configuration Reference](./CONFIGURATION.md) - All configuration options
- [Getting Started](./GETTING_STARTED.md) - Installation and initial setup
- [GitHub Issues](https://github.com/Jings/hass-coolify-monitor/issues) - Report problems
