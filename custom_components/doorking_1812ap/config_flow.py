"""Adds config flow for Blueprint."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    Doorking1812APApiClient,
    Doorking1812APApiClientCommunicationError,
    Doorking1812APApiClientError,
)
from .const import DOMAIN, LOGGER


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_connection(
                    ip_address=user_input[CONF_IP_ADDRESS],
                )
            except Doorking1812APApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except Doorking1812APApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_IP_ADDRESS],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IP_ADDRESS,
                        default=(user_input or {}).get(CONF_IP_ADDRESS, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self, ip_address: str) -> None:
        """Validate credentials."""
        client = Doorking1812APApiClient(
            ip_address=ip_address,
            session=async_create_clientsession(self.hass),
        )

        # connect to server
        # try to read gate status

        await client.async_get_state()
