from pydantic import validate_call
from starlette.datastructures import URL
from fastapi import Request


@validate_call(config={"arbitrary_types_allowed": True})
def get_relative_url(val: Request | URL) -> str:
    """Get relative url only path with query params from request object or URL object.

    Args:
        val (Request | URL, required): Request object or URL object to extract relative url.

    Returns:
        str: Relative url only path with query params.
    """

    if isinstance(val, Request):
        val = val.url

    _relative_url = str(val).replace(f"{val.scheme}://{val.netloc}", "")
    return _relative_url


@validate_call(config={"arbitrary_types_allowed": True})
def get_base_url(val: Request | URL) -> str:
    """Get base url only scheme and netloc from request object or URL object.

    Args:
        val (Request | URL, required): Request object or URL object to extract base url.

    Returns:
        str: Base url only scheme and netloc.
    """

    _base_url = ""
    if isinstance(val, Request):
        _base_url = str(val.base_url)[:-1]
    else:
        _base_url = f"{val.scheme}://{val.netloc}"

    return _base_url


__all__ = [
    "get_relative_url",
    "get_base_url",
]
