"""Switch platform for doorking_1812ap."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import Doorking1812APEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import Doorking1812APDataUpdateCoordinator
    from .data import Doorking1812APConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="doorking_1812ap",
        name="Doorking 1812AP",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: Doorking1812APConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        Doorking1812APSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class Doorking1812APSwitch(Doorking1812APEntity, SwitchEntity):
    """doorking_1812ap switch class."""

    def __init__(
        self,
        coordinator: Doorking1812APDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get("title", "") == "foo"

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        await self.coordinator.config_entry.runtime_data.client.async_set_title("bar")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        await self.coordinator.config_entry.runtime_data.client.async_set_title("foo")
        await self.coordinator.async_request_refresh()
