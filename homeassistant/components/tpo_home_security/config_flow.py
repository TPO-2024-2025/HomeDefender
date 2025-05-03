"""Config flow for the tpo_home_security integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries

# 1) IMPORT THE REAL BASE CLASS (aliased so we can still call ours ConfigFlow)
from homeassistant.config_entries import ConfigFlow as _ConfigFlow, ConfigFlowResult
from homeassistant.const import (  # noqa: F401
    CONF_EMAIL,
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class PlaceholderHub:
    """Placeholder class to make tests pass."""

    def __init__(self, host: str) -> None:  # noqa: D107
        self.host = host

    async def authenticate(self, username: str, password: str) -> bool:  # noqa: D102
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:  # noqa: D103
    hub = PlaceholderHub(data[CONF_HOST])
    if not await hub.authenticate(data[CONF_USERNAME], data[CONF_PASSWORD]):
        raise InvalidAuth
    return {"title": "Name of the device"}


# 2) SUBCLASS THE ALIASED BASE CLASS, NOT undefined ConfigFlow
class ConfigFlow(_ConfigFlow, domain=DOMAIN):
    """Handle a config flow for tpo_home_security."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # 3) THESE BOTH RETURN Any → SILENCE IT
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    # 4) Tell HA there *is* an options flow
    @staticmethod
    def async_get_options_flow(config_entry):  # noqa: D102
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Allows editing email_recipients (and later other options) at runtime."""

    def __init__(self, config_entry):  # noqa: D107
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Initial options step."""  # noqa: D401
        if user_input is not None:
            # store updated recipients in entry.options
            return self.async_create_entry(title="", data=user_input)

        # build form schema, defaulting to current recipients
        current = self.config_entry.options.get("email_recipients", [])
        schema = vol.Schema(
            {
                # list of emails; use voluptuous’s email validator
                vol.Optional("email_recipients", default=current): vol.All(
                    cv.ensure_list, [cv.email]
                )
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
