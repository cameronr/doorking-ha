"""Custom types for doorking_1812ap."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import Doorking1812APApiClient
    from .coordinator import Doorking1812APDataUpdateCoordinator


type Doorking1812APConfigEntry = ConfigEntry[Doorking1812APData]


@dataclass
class Doorking1812APData:
    """Data for the Blueprint integration."""

    client: Doorking1812APApiClient
    coordinator: Doorking1812APDataUpdateCoordinator
    integration: Integration
