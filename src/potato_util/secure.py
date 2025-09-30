import hashlib

from pydantic import validate_call

from .constants import HashAlgoEnum


@validate_call
def hash_str(
    val: str | bytes, algorithm: HashAlgoEnum | str = HashAlgoEnum.sha256
) -> str:
    """Hash a string using a specified hash algorithm.

    Args:
        val       (str | bytes       , required): The value to be hashed.
        algorithm (HashAlgoEnum | str, optional): The hash algorithm to use. Defaults to `HashAlgoEnum.sha256`.

    Returns:
        str: The hexadecimal representation of the digest.
    """

    if isinstance(val, str):
        val = val.encode("utf-8")

    if isinstance(algorithm, str):
        algorithm = HashAlgoEnum(algorithm.strip().lower())

    _hash = hashlib.new(algorithm.value)
    _hash.update(val)

    _hash_val = _hash.hexdigest()
    return _hash_val


__all__ = [
    "hash_str",
]
