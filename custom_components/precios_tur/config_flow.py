"""Minimal Config Flow for Precios TUR."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.const import CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

from .const import DEFAULT_URL, DOMAIN

CATEGORY_OPTIONS = ["TUR1", "TUR2", "TUR3"]

class PreciosTurConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Precios TUR."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                await self._validate_api_connection(user_input.get(CONF_URL, DEFAULT_URL))
                category = user_input.get("category", "TUR1")
                return self.async_create_entry(
                    title=f"Precios TUR - {category}",
                    data=user_input
                )
            except ValueError as err:
                _LOGGER.error(f"Validation error: {err}")
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_URL, default=DEFAULT_URL): str,
            vol.Required("category", default="TUR1"): vol.In(CATEGORY_OPTIONS)
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    async def _validate_api_connection(self, url: str) -> None:
        """Validate the API connection."""
        try:
            session = async_get_clientsession(self.hass)

            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error(f"API returned status code {response.status}")
                    raise ValueError(f"API returned status code {response.status}")

                # Try to parse JSON
                data = await response.json()

                # Basic validation of the response structure
                if not data or 'data' not in data or not data['data']:
                    _LOGGER.error("Invalid API response structure")
                    raise ValueError("Invalid API response structure")

        except aiohttp.ClientError as err:
            _LOGGER.error(f"Connection error: {err}")
            raise ValueError("Cannot connect to API") from err
        except ValueError as err:
            _LOGGER.error(f"JSON parsing error: {err}")
            raise ValueError("Invalid JSON response") from err