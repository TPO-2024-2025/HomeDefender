"""The tpo_home_security integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .listener import register_listeners

_PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up tpo_home_security from a config entry."""
    # If you later have an API object, you can do:
    # api = MyApi(entry.data["host"], entry.data["username"], entry.data["password"])
    # entry.runtime_data["api"] = api

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up tpo_home_security for YAML-based configuration (if used)."""
    register_listeners(hass)
    return True
