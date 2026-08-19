"""Options flow for coolify_monitor."""

from typing import Any

from custom_components.coolify_monitor.api import CoolifyMonitorApiClientError
from custom_components.coolify_monitor.const import CONF_SELECTED_RESOURCES, LOGGER
from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_URL

from .handler import async_discover_resources
from .schemas import build_selected_resources, get_options_schema, get_resources_schema


class CoolifyMonitorOptionsFlow(config_entries.OptionsFlow):
    """Let the user change the poll interval or which resources are monitored."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Offer a choice between the two things this options flow can change.

        Returns:
            The menu.

        """
        return self.async_show_menu(
            step_id="init",
            menu_options=["update_interval", "resources"],
        )

    async def async_step_update_interval(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Show and process the update-interval form.

        Returns:
            The form, or the stored options.

        """
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={**self.config_entry.options, **user_input},
            )

        return self.async_show_form(
            step_id="update_interval",
            data_schema=get_options_schema(self.config_entry.options),
        )

    async def async_step_resources(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Re-run discovery and let the user adjust which resources are monitored.

        Returns:
            The form, the stored options, or the abort that follows a failed discovery.

        """
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    **self.config_entry.options,
                    CONF_SELECTED_RESOURCES: build_selected_resources(user_input),
                },
            )

        try:
            discovered = await async_discover_resources(
                self.hass,
                url=self.config_entry.data[CONF_URL],
                api_token=self.config_entry.data[CONF_API_TOKEN],
            )
        except CoolifyMonitorApiClientError:
            return self.async_abort(reason="discovery_failed")
        except Exception:  # noqa: BLE001 - Anything unexpected still has to abort cleanly.
            LOGGER.exception("Unexpected exception")
            return self.async_abort(reason="discovery_failed")

        return self.async_show_form(
            step_id="resources",
            data_schema=get_resources_schema(
                discovered,
                selected=self.config_entry.options.get(CONF_SELECTED_RESOURCES),
            ),
            description_placeholders={
                "server_count": str(len(discovered["servers"])),
                "application_count": str(len(discovered["applications"])),
                "database_count": str(len(discovered["databases"])),
                "team_count": str(len(discovered["teams"])),
                "service_count": str(len(discovered["services"])),
            },
        )


__all__ = ["CoolifyMonitorOptionsFlow"]
