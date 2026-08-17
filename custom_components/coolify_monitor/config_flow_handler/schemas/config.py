"""Config flow schemas for the user, reconfigure and reauth steps."""

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.const import CONF_API_TOKEN, CONF_URL
from homeassistant.helpers import selector

_URL_SELECTOR = selector.TextSelector(
    selector.TextSelectorConfig(type=selector.TextSelectorType.URL),
)
_API_TOKEN_SELECTOR = selector.TextSelector(
    selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD),
)


def get_user_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Build the schema for the user step.

    Args:
        defaults: Previously submitted values, used to pre-fill the form.

    Returns:
        The voluptuous schema for the connection form.

    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_URL,
                default=defaults.get(CONF_URL, vol.UNDEFINED),
            ): _URL_SELECTOR,
            vol.Required(CONF_API_TOKEN): _API_TOKEN_SELECTOR,
        },
    )


def get_reconfigure_schema(url: str) -> vol.Schema:
    """
    Build the schema for the reconfigure step.

    Args:
        url: The entry's current instance URL, used to pre-fill the form.

    Returns:
        The voluptuous schema for the reconfigure form.

    """
    return vol.Schema(
        {
            vol.Required(CONF_URL, default=url): _URL_SELECTOR,
            vol.Required(CONF_API_TOKEN): _API_TOKEN_SELECTOR,
        },
    )


def get_reauth_schema(url: str) -> vol.Schema:
    """
    Build the schema for the reauth step.

    Args:
        url: The entry's current instance URL, used to pre-fill the form.

    Returns:
        The voluptuous schema for the reauth form.

    """
    return vol.Schema(
        {
            vol.Required(CONF_URL, default=url): _URL_SELECTOR,
            vol.Required(CONF_API_TOKEN): _API_TOKEN_SELECTOR,
        },
    )


__all__ = [
    "get_reauth_schema",
    "get_reconfigure_schema",
    "get_user_schema",
]
