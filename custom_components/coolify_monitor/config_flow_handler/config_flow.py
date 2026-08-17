"""Config flow for coolify_monitor — user setup, reconfigure and reauth."""

from typing import Any

from custom_components.coolify_monitor.api import (
    CoolifyMonitorApiClientAuthenticationError,
    CoolifyMonitorApiClientCommunicationError,
)
from custom_components.coolify_monitor.const import DOMAIN, LOGGER
from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_URL
from homeassistant.loader import async_get_loaded_integration

from .options_flow import CoolifyMonitorOptionsFlow
from .schemas import get_reauth_schema, get_reconfigure_schema, get_user_schema
from .validators import validate_connection


class CoolifyMonitorConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for coolify_monitor."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> CoolifyMonitorOptionsFlow:
        """
        Return the options flow for this handler.

        Returns:
            The options flow instance.

        """
        return CoolifyMonitorOptionsFlow()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle a flow started by the user.

        Returns:
            The form, or the created config entry.

        """
        errors: dict[str, str] = {}

        if user_input is not None:
            unique_id, errors = await self._async_validate(user_input)
            if not errors and unique_id is not None:
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_URL],
                    data=user_input,
                )

        integration = async_get_loaded_integration(self.hass, DOMAIN)

        return self.async_show_form(
            step_id="user",
            data_schema=get_user_schema(user_input),
            errors=errors,
            description_placeholders={
                "documentation_url": integration.documentation or "",
            },
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle reconfiguration of an existing entry.

        Returns:
            The form, or the abort that follows the entry update.

        """
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            unique_id, errors = await self._async_validate(user_input)
            if not errors and unique_id is not None:
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(entry, data_updates=user_input)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                get_reconfigure_schema(entry.data.get(CONF_URL, "")),
                entry.data,
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self,
        entry_data: dict[str, Any],
    ) -> config_entries.ConfigFlowResult:
        """
        Start reauthentication after the coordinator reported an invalid token.

        Returns:
            The result of the reauth_confirm step.

        """
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Collect and verify a replacement API token.

        Returns:
            The form, or the abort that follows the entry update.

        """
        entry = self._get_reauth_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            unique_id, errors = await self._async_validate(user_input)
            if not errors and unique_id is not None:
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(entry, data_updates=user_input)

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=get_reauth_schema(entry.data.get(CONF_URL, "")),
            errors=errors,
            description_placeholders={
                "url": entry.data.get(CONF_URL, ""),
            },
        )

    async def _async_validate(self, user_input: dict[str, Any]) -> tuple[str | None, dict[str, str]]:
        """
        Test the submitted connection details.

        Returns:
            The discovered unique ID and an empty errors dict when they work,
            otherwise None and the errors for the form.

        """
        try:
            unique_id = await validate_connection(
                self.hass,
                url=user_input[CONF_URL],
                api_token=user_input[CONF_API_TOKEN],
            )
        except CoolifyMonitorApiClientAuthenticationError:
            return None, {"base": "invalid_auth"}
        except CoolifyMonitorApiClientCommunicationError:
            return None, {"base": "cannot_connect"}
        except Exception:  # noqa: BLE001 - Anything unexpected still has to reach the form.
            LOGGER.exception("Unexpected exception")
            return None, {"base": "unknown"}

        return unique_id, {}


__all__ = ["CoolifyMonitorConfigFlowHandler"]
