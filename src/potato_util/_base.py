import re
import copy
import logging

from pydantic import validate_call


logger = logging.getLogger(__name__)


@validate_call
def deep_merge(dict1: dict, dict2: dict) -> dict:
    """Return a new dictionary that's the result of a deep merge of two dictionaries.
    If there are conflicts, values from `dict2` will overwrite those in `dict1`.

    Args:
        dict1 (dict, required): The base dictionary that will be merged.
        dict2 (dict, required): The dictionary to merge into `dict1`.

    Returns:
        dict: The merged dictionary.
    """

    _merged = copy.deepcopy(dict1)
    for _key, _val in dict2.items():
        if (
            _key in _merged
            and isinstance(_merged[_key], dict)
            and isinstance(_val, dict)
        ):
            _merged[_key] = deep_merge(_merged[_key], _val)
        else:
            _merged[_key] = copy.deepcopy(_val)

    return _merged


@validate_call
def camel_to_snake(val: str) -> str:
    """Convert CamelCase to snake_case.

    Args:
        val (str): CamelCase string to convert.

    Returns:
        str: Converted snake_case string.
    """

    val = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", val)
    val = re.sub("([a-z0-9])([A-Z])", r"\1_\2", val).lower()
    return val


__all__ = [
    "deep_merge",
    "camel_to_snake",
]
