import uuid
import string
import secrets

from pydantic import validate_call

from .dt import now_ts


@validate_call
def gen_unique_id(prefix: str = "") -> str:
    """Generate unique ID. Format: '{prefix}{datetime}_{uuid4}'.

    Args:
        prefix (str, optional): Prefix of ID. Defaults to ''.

    Raises:
        ValueError: If `prefix` length is greater than 32.

    Returns:
        str: Unique ID.
    """

    prefix = prefix.strip()
    if 32 < len(prefix):
        raise ValueError(
            f"`prefix` argument length {len(prefix)} is too long, must be less than or equal to 32!",
        )

    _id = str(f"{prefix}{now_ts()}_{uuid.uuid4().hex}").lower()
    return _id


@validate_call
def gen_random_string(
    length: int = 16,
    digits: bool = True,
    ascii_letters: bool = True,
    punctuation: bool = False,
) -> str:
    """Generate secure random string.

    Args:
        length        (int , optional): Length of random string. Defaults to 16.
        digits        (bool, optional): If True, include digits. Defaults to True.
        ascii_letters (bool, optional): If True, include ASCII letters. Defaults to True.
        punctuation   (bool, optional): If True, include punctuation characters. Defaults to False.

    Raises:
        ValueError: If `length` is less than 1.
        ValueError: If all of `digits`, `ascii_letters`, and `punctuation` are False.

    Returns:
        str: Generated random string.
    """

    if length < 1:
        raise ValueError(
            f"`length` argument value {length} is too small, must be greater than or equal to 1!",
        )

    _base_chars = ""
    if digits:
        _base_chars += string.digits
    if ascii_letters:
        _base_chars += string.ascii_letters
    if punctuation:
        _base_chars += string.punctuation

    if not _base_chars:
        raise ValueError(
            "At least one of `digits`, `ascii_letters`, or `punctuation` must be True!"
        )

    _random_str = "".join(secrets.choice(_base_chars) for _ in range(length))
    return _random_str


__all__ = [
    "gen_unique_id",
    "gen_random_string",
]
