from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import validate_call, SecretStr


@validate_call
def hash(password: SecretStr, password_pepper: SecretStr | None = None) -> str:
    """Hashes password with salt and pepper using Argon2id.

    Args:
        password        (SecretStr, required): Password to hash.
        password_pepper (SecretStr, optional): Pepper to hash password with. Defaults to None.

    Returns:
        str: Hashed password.
    """

    _ph = PasswordHasher()
    _seasoned_password = password.get_secret_value()
    if password_pepper:
        _seasoned_password = _seasoned_password + password_pepper.get_secret_value()

    _hash_password = _ph.hash(_seasoned_password)
    return _hash_password


@validate_call
def verify(
    hashed_password: str, password: SecretStr, password_pepper: SecretStr | None = None
) -> bool:
    """Verifies password with salt and pepper against hashed password using Argon2id.

    Args:
        hashed_password (str      , required): Hashed password.
        password        (SecretStr, required): Raw password to verify.
        password_pepper (SecretStr, optional): Pepper to verify password with. Defaults to None.

    Returns:
        bool: True if password is match, False otherwise.
    """

    _ph = PasswordHasher()
    _seasoned_password = password.get_secret_value()
    if password_pepper:
        _seasoned_password = _seasoned_password + password_pepper.get_secret_value()

    try:
        _ph.verify(hashed_password, _seasoned_password)
        return True
    except VerifyMismatchError:
        return False


__all__ = [
    "hash",
    "verify",
]
