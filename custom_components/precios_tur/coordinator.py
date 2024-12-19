"""Data update coordinator for Precios TUR."""

import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    ATTR_FIXED_RATE,
    ATTR_PRICE_DATE,
    ATTR_VARIABLE_RATE,
    DOMAIN,
    UPDATE_INTERVAL_SECONDS,
)

_LOGGER = logging.getLogger(__name__)
HTTP_OK = 200


class PreciosTurCoordinator(DataUpdateCoordinator):
    """Class to manage fetching gas price data from the API."""

    def __init__(self, hass: HomeAssistant, url: str, category: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.url = url
        self.category = category

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        try:
            session = async_get_clientsession(self.hass)
            _LOGGER.debug(f"Fetching data from {self.url}")
            async with session.get(self.url) as response:
                _LOGGER.debug(f"Response status: {response.status}")
                if response.status != HTTP_OK:
                    msg = f"API returned {response.status}"
                    raise UpdateFailed(msg)  # noqa: TRY301

                data = await response.json()

                # Find the entry matching the specified category
                matching_entries = [entry for entry in data.get("data", []) if entry.get("category") == self.category]

                _LOGGER.debug(f"Found {len(matching_entries)} entries for category {self.category}")
                if not matching_entries:
                    msg = f"No data found for category {self.category}"
                    raise UpdateFailed(msg)  # noqa: TRY301

                entry = matching_entries[0]
                _LOGGER.debug(f"Entry: {entry}")

                return {
                    ATTR_VARIABLE_RATE: entry.get("variableRate", 0),
                    ATTR_FIXED_RATE: entry.get("fixedRate", 0),
                    ATTR_PRICE_DATE: entry.get("date"),
                }

        except aiohttp.ClientError as err:
            _LOGGER.exception("Connection error")
            msg = f"Connection error: {err}"
            raise UpdateFailed(msg) from err
        except ValueError as err:
            _LOGGER.exception("JSON parsing error")
            msg = f"Invalid JSON response: {err}"
            raise UpdateFailed(msg) from err
        except Exception as err:
            _LOGGER.exception("Unexpected error in data update")
            msg = f"Unexpected error: {err}"
            raise UpdateFailed(msg) from err
