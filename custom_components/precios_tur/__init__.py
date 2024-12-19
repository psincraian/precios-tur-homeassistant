"""Minimal initialization for Precios TUR."""

from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_URL
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN
from .sensor import PreciosTurCoordinator
PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    _LOGGER.info("Setting up Precios TUR entry")

    # Create the coordinator
    coordinator = PreciosTurCoordinator(hass, entry.data[CONF_URL], entry.data["category"])
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator in hass.data
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward the setup to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Precios TUR entry")
    return True