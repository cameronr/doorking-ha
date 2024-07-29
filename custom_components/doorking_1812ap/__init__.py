"""
Custom integration to integrate doorking_1812ap with Home Assistant.

For more details about this integration, please refer to
https://github.com/cameronr/doorking-ha
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import CONF_IP_ADDRESS, Platform
from homeassistant.loader import async_get_loaded_integration

from .api import Doorking1812APApiClient
from .coordinator import Doorking1812APDataUpdateCoordinator
from .data import Doorking1812APData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import Doorking1812APConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: Doorking1812APConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = Doorking1812APDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = Doorking1812APData(
        client=Doorking1812APApiClient(
            ip_address=entry.data[CONF_IP_ADDRESS],
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: Doorking1812APConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: Doorking1812APConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
