"""Sample API Client."""

from __future__ import annotations

import asyncio
import socket
from typing import Any

from .const import LOGGER


class Doorking1812APApiClientError(Exception):
    """Exception to indicate a general API error."""


class Doorking1812APApiClientCommunicationError(
    Doorking1812APApiClientError,
):
    """Exception to indicate a communication error."""


UNEXPECTED_DATA_ERROR = "Unexpected data received: {}"


def _raise_unexpected_data_error(data: bytes) -> None:
    """Raise a ValueError for unexpected data."""
    error_message = UNEXPECTED_DATA_ERROR.format(data)
    raise ValueError(error_message)


class Doorking1812APApiClient:
    """Sample API Client."""

    PORT = 1030

    def __init__(
        self,
        ip_address: str,
    ) -> None:
        """Sample API Client."""
        self._ip_address = ip_address

    async def connect_to_server(
        self,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Connect to the Doorking 1812AP."""
        retries = 5
        delay = 1
        for attempt in range(1, retries + 1):
            try:
                reader, writer = await asyncio.open_connection(
                    self._ip_address, self.PORT
                )
            except (TimeoutError, OSError, socket.gaierror) as e:
                LOGGER.debug(f"Attempt {attempt} failed: {e}")
                if attempt < retries:
                    LOGGER.debug(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    LOGGER.debug("All retries failed.")
                    msg = f"Timeout connecting to server - {e}"
                    raise Doorking1812APApiClientCommunicationError(
                        msg,
                    ) from e
            else:
                LOGGER.debug(
                    f"Connected to {self._ip_address}:{self.PORT} on attempt {attempt}"
                )
                return reader, writer
        raise Exception  # noqa: TRY002, unreachable

    async def async_get_data(self) -> Any:
        """Get open status from gate controller."""
        try:
            LOGGER.debug("getting state")
            state = {}
            reader, writer = await self.connect_to_server()
            # This byte sequence requests status
            message = b"\x01\x10\x03"
            writer.write(message)
            await writer.drain()

            # Read 7 bytes of data from the server
            data = await reader.readexactly(7)

            writer.close()
            await writer.wait_closed()

            if data == b"\x10\x10\x07\x80\x00\x80\x00":
                LOGGER.debug("gate is open")
                state["open"] = True
                return state

            if data == b"\x10\x10\x07\x00\x00\x00\x00":
                state["open"] = False
                LOGGER.debug("gate is closed")
                return state

            LOGGER.debug("gate is unknown")
            _raise_unexpected_data_error(data)

        except Doorking1812APApiClientCommunicationError:
            raise
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise Doorking1812APApiClientError(
                msg,
            ) from exception

    async def async_open_gate(self, *, close_gate: bool = False) -> Any:
        """Open or close gate."""
        try:
            _, writer = await self.connect_to_server()
            data = b"\x01\x11\x05\x00\x80" if close_gate else b"\x01\x11\x05\x01\x80"

            LOGGER.debug(f"set gate open/close: {close_gate}")

            # We spam the message 3 times just in case
            for _ in range(3):
                writer.write(data)
                await writer.drain()

            writer.close()
            await writer.wait_closed()

        except Doorking1812APApiClientCommunicationError:
            raise
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise Doorking1812APApiClientError(
                msg,
            ) from exception
