"""Data update coordinator for Precios TUR."""

import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    UPDATE_INTERVAL_SECONDS,
    ATTR_VARIABLE_RATE,
    ATTR_FIXED_RATE,
    ATTR_PRICE_DATE,
)

_LOGGER = logging.getLogger(__name__)

class PreciosTurCoordinator(DataUpdateCoordinator):
    """Class to manage fetching gas price data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        url: str,
        category: str
    ):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS)
        )
        self.url = url
        self.category = category

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            session = async_get_clientsession(self.hass)
            _LOGGER.debug(f"Fetching data from {self.url}")
            async with session.get(self.url) as response:
                _LOGGER.debug(f"Response status: {response.status}")
                if response.status != 200:
                    raise UpdateFailed(f"API returned {response.status}")

                data = await response.json()

                # Find the entry matching the specified category
                matching_entries = [
                    entry for entry in data.get('data', [])
                    if entry.get('category') == self.category
                ]

                _LOGGER.debug(f"Found {len(matching_entries)} entries for category {self.category}")    
                if not matching_entries:
                    raise UpdateFailed(f"No data found for category {self.category}")

                entry = matching_entries[0]
                _LOGGER.debug(f"Entry: {entry}")
                
                return {
                    ATTR_VARIABLE_RATE: entry.get('variableRate', 0),
                    ATTR_FIXED_RATE: entry.get('fixedRate', 0),
                    ATTR_PRICE_DATE: entry.get('date')
                }

        except aiohttp.ClientError as err:
            _LOGGER.error(f"Connection error: {err}")
            raise UpdateFailed(f"Connection error: {err}") from err
        except ValueError as err:
            _LOGGER.error(f"JSON parsing error: {err}")
            raise UpdateFailed(f"Invalid JSON response: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error in data update")
            raise UpdateFailed(f"Unexpected error: {err}") from err