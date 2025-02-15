from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_movies import PaginatedMovies
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
    query: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/movies/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedMovies]]:
    if response.status_code == 200:
        response_200 = PaginatedMovies.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, PaginatedMovies]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
    query: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedMovies]]:
    """Get Movies

    Args:
        skip (Union[Unset, int]): Number of items to skip Default: 0.
        limit (Union[Unset, int]): Number of items to retrieve Default: 10.
        query (Union[Unset, str]): Search query

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code
        and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedMovies]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
    query: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedMovies]]:
    """Get Movies

    Args:
        skip (Union[Unset, int]): Number of items to skip Default: 0.
        limit (Union[Unset, int]): Number of items to retrieve Default: 10.
        query (Union[Unset, str]): Search query

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code
        and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedMovies]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
    query: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedMovies]]:
    """Get Movies

    Args:
        skip (Union[Unset, int]): Number of items to skip Default: 0.
        limit (Union[Unset, int]): Number of items to retrieve Default: 10.
        query (Union[Unset, str]): Search query

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code
         and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedMovies]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
    query: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedMovies]]:
    """Get Movies

    Args:
        skip (Union[Unset, int]): Number of items to skip Default: 0.
        limit (Union[Unset, int]): Number of items to retrieve Default: 10.
        query (Union[Unset, str]): Search query

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code
        and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedMovies]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            query=query,
        )
    ).parsed
