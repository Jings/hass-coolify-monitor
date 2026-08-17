"""API client for coolify_monitor."""

import asyncio
import socket
from typing import Any

import aiohttp

API_BASE_PATH = "/api/v1"
REQUEST_TIMEOUT = 15


class CoolifyMonitorApiClientError(Exception):
    """Base exception to indicate a general API error."""


class CoolifyMonitorApiClientCommunicationError(
    CoolifyMonitorApiClientError,
):
    """Exception to indicate a communication error with the API."""


class CoolifyMonitorApiClientAuthenticationError(
    CoolifyMonitorApiClientError,
):
    """Exception to indicate an authentication error with the API."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """
    Verify that the API response is valid.

    Raises:
        CoolifyMonitorApiClientAuthenticationError: For 401 and 403 responses.
        aiohttp.ClientResponseError: For every other unsuccessful status.

    """
    if response.status in (401, 403):
        msg = "Invalid or revoked API token"
        raise CoolifyMonitorApiClientAuthenticationError(msg)
    response.raise_for_status()


class CoolifyMonitorApiClient:
    """Thin async client for the Coolify REST API (`/api/v1`)."""

    def __init__(
        self,
        base_url: str,
        api_token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._base_url = base_url.rstrip("/")
        self._api_token = api_token
        self._session = session

    async def async_get_servers(self) -> list[dict[str, Any]]:
        """
        Fetch every server known to this Coolify instance.

        Returns:
            The raw server list, exactly as Coolify returns it.

        """
        return await self._api_wrapper("get", "/servers")

    async def async_get_applications(self) -> list[dict[str, Any]]:
        """
        Fetch every application known to this Coolify instance.

        Returns:
            The raw application list, exactly as Coolify returns it.

        """
        return await self._api_wrapper("get", "/applications")

    async def async_get_databases(self) -> list[dict[str, Any]]:
        """
        Fetch every database known to this Coolify instance.

        Returns:
            The raw database list, exactly as Coolify returns it.

        """
        return await self._api_wrapper("get", "/databases")

    async def _api_wrapper(self, method: str, path: str) -> Any:
        """
        Perform a request and translate transport errors into client exceptions.

        Returns:
            The decoded JSON response.

        Raises:
            CoolifyMonitorApiClientAuthenticationError: If the token is rejected.
            CoolifyMonitorApiClientCommunicationError: If the request does not complete.
            CoolifyMonitorApiClientError: For any other failure.

        """
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.request(
                    method=method,
                    url=f"{self._base_url}{API_BASE_PATH}{path}",
                    headers={"Authorization": f"Bearer {self._api_token}"},
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise CoolifyMonitorApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise CoolifyMonitorApiClientCommunicationError(msg) from exception
        except CoolifyMonitorApiClientError:
            raise
        except Exception as exception:
            msg = f"Unexpected error talking to the API - {exception}"
            raise CoolifyMonitorApiClientError(msg) from exception
