"""Sensor platform for Precios TUR."""

import logging
from collections.abc import Coroutine
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CURRENCY_EURO,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.translation import async_get_translations

from .const import (
    ATTR_FIXED_RATE,
    ATTR_PRICE_DATE,
    ATTR_VARIABLE_RATE,
    DOMAIN,
)
from .coordinator import PreciosTurCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors from a config entry."""
    # Retrieve the coordinator from the config entry
    coordinator: PreciosTurCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug(f"Setting up sensors for {coordinator.category}")
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug(f"Data: {coordinator.data}")

    # Retrieve translations
    user_language = hass.config.language
    _LOGGER.debug(f"User language: {user_language}")
    translations = await async_get_translations(hass, user_language, "sensor", [DOMAIN])

    # Create sensor entities
    entities = [
        PreciosTurSensor(
            coordinator,
            ATTR_VARIABLE_RATE,
            translations.get(
                f"component.{DOMAIN}.entity.sensor.variable_rate.name",
                "Variable Rate Hardcoded",
            ),
            config_entry.entry_id,
            config_entry.data["category"],
        ),
        PreciosTurSensor(
            coordinator,
            ATTR_FIXED_RATE,
            translations.get(f"component.{DOMAIN}.entity.sensor.fixed_rate.name", "Fixed Rate"),
            config_entry.entry_id,
            config_entry.data["category"],
        ),
    ]

    async_add_entities(entities)


class PreciosTurSensor(SensorEntity):
    """Representation of a Gas Price Sensor."""

    def __init__(
        self,
        coordinator: PreciosTurCoordinator,
        rate_type: str,
        translated_name: str,
        entry_id: str,
        category: str,
    ) -> PreciosTurCoordinator:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._rate_type = rate_type
        self._entry_id = entry_id
        self._category = category

        # Construct unique identifier and name
        self._attr_unique_id = f"{DOMAIN}_{rate_type}_{entry_id}_{category}"
        self._attr_name = translated_name

        # Sensor configuration
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = CURRENCY_EURO if rate_type == ATTR_FIXED_RATE else "EUR/kWh"

    @property
    def available(self) -> bool:
        """Return if sensor is available."""
        return self._coordinator.last_update_success and self._coordinator.data is not None

    @property
    def state(self) -> Any:
        """Return the state of the sensor."""
        return self._coordinator.data.get(self._rate_type) if self._coordinator.data else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes."""
        if not self._coordinator.data:
            return {}

        return {
            "date": self._coordinator.data.get(ATTR_PRICE_DATE),
            "source_url": self._coordinator.url,
            "category": self._coordinator.category,
        }

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for data updates."""
        self.async_on_remove(self._coordinator.async_add_listener(self.async_write_ha_state))

    async def async_update(self) -> Coroutine[Any, Any, None]:
        """Update the sensor."""
        await self._coordinator.async_request_refresh()
