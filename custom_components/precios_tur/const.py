"""Constants for precios_tur."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)


"""Constants for the Precios TUR integration."""

# Configuration keys
DOMAIN = "precios_tur"
CONF_CATEGORY = "category"

# Default values
DEFAULT_URL = "https://precios-tur.petru.tech/api/v1/prices/current"
DEFAULT_CATEGORY = "TUR1"

# Update intervals
UPDATE_INTERVAL_SECONDS = 12 * 60 * 60  # 12 hours

# Attributes
ATTR_VARIABLE_RATE = "variable_rate"
ATTR_FIXED_RATE = "fixed_rate"
ATTR_PRICE_DATE = "price_date"

# Error messages
ERROR_CANNOT_CONNECT = "cannot_connect"
ERROR_INVALID_RESPONSE = "invalid_response"

# Unique identifier prefix
UNIQUE_ID_PREFIX = f"{DOMAIN}_"
