"""Constants for doorking_1812ap."""

from datetime import timedelta
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "doorking_1812ap"

SCAN_INTERVAL = timedelta(seconds=30)
