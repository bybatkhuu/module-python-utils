import base64
import logging
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import validate_call

from ...constants import WarnEnum

logger = logging.getLogger(__name__)


@validate_call
def gen_key(
    bit_length: int = 256, return_str: bool = False, base64_encode: bool = True
) -> str | bytes:
    """Generates a random AES-GCM key.

    Args:
        bit_length    (int, optional): The length of the key in bits. Defaults to 256 (32 bytes).
        return_str    (bool, optional): Whether to return the key as a string. Defaults to False.
        base64_encode (bool, optional): Whether to base64 encode the key if returning as a string. Defaults to True.

    Returns:
        str | bytes: The generated AES-GCM key.
    """

    _key = AESGCM.generate_key(bit_length=bit_length)
    if return_str:
        if base64_encode:
            _key = base64.b64encode(_key).decode()
        else:
            _key = _key.hex()

    return _key


@validate_call
def encrypt(
    key: bytes,
    plaintext: str | bytes,
    aad: str | bytes | None = None,
    nonce_nbytes: int = 12,
    base64_encode: bool = False,
    return_str: bool = False,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> tuple[str | bytes, str | bytes]:
    """Encrypts plaintext using AES-GCM key and nonce.

    Args:
        key           (bytes             , required): The encryption key.
        plaintext     (str | bytes       , required): The data to be encrypted.
        aad           (str | bytes | None, optional): Additional authenticated data. Defaults to None.
        nonce_nbytes  (int               , optional): The number of bytes for the nonce. Defaults to 12.
        base64_encode (bool              , optional): Whether to base64 encode the nonce and ciphertext.
                                                        Defaults to False.
        return_str    (bool              , optional): Whether to return the result as a string. Defaults to False.
        warn_mode     (WarnEnum          , optional): The warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        Exception: If failed to encrypt plaintext using AES-GCM key and nonce for any reason.

    Returns:
        tuple[str | bytes, str | bytes]: The nonce and ciphertext resulting from the encryption.
    """

    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    if isinstance(aad, str):
        aad = aad.encode()

    _message = "Encrypting plaintext using AES-GCM key and nonce..."
    if warn_mode == WarnEnum.ALWAYS:
        logger.info(_message)
    elif warn_mode == WarnEnum.DEBUG:
        logger.debug(_message)

    _nonce: str | bytes
    _ciphertext: str | bytes
    try:
        _aes_gcm = AESGCM(key=key)
        _nonce = secrets.token_bytes(nbytes=nonce_nbytes)
        _ciphertext = _aes_gcm.encrypt(
            nonce=_nonce, data=plaintext, associated_data=aad
        )

        _message = "Successfully encrypted plaintext using AES-GCM key and nonce."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    except Exception:
        _message = "Failed to encrypt plaintext using AES-GCM key and nonce!"
        if warn_mode == WarnEnum.ALWAYS:
            logger.error(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        raise

    if base64_encode:
        _nonce = base64.b64encode(_nonce)
        _ciphertext = base64.b64encode(_ciphertext)

    if return_str:
        _nonce = _nonce.decode()
        _ciphertext = _ciphertext.decode()

    return _nonce, _ciphertext


@validate_call
def decrypt(
    key: bytes,
    nonce: str | bytes,
    ciphertext: str | bytes,
    aad: str | bytes | None = None,
    base64_decode: bool = False,
    return_str: bool = False,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> str | bytes:
    """Decrypts ciphertext using AES-GCM key and nonce.

    Args:
        key           (bytes             , required): The decryption key.
        nonce         (str | bytes       , required): The nonce used during encryption.
        ciphertext    (str | bytes       , required): The data to be decrypted.
        aad           (str | bytes | None, optional): Additional authenticated data. Defaults to None.
        base64_decode (bool              , optional): Whether to base64 decode the nonce and ciphertext.
                                                        Defaults to False.
        return_str    (bool              , optional): Whether to return the result as a string. Defaults to False.
        warn_mode     (WarnEnum          , optional): The warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        Exception: If failed to decrypt ciphertext using AES-GCM key and nonce for any reason.

    Returns:
        str | bytes: The decrypted plaintext.
    """

    if isinstance(nonce, str):
        nonce = nonce.encode()

    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()

    if isinstance(aad, str):
        aad = aad.encode()

    if base64_decode:
        nonce = base64.b64decode(nonce)
        ciphertext = base64.b64decode(ciphertext)

    _message = "Decrypting ciphertext using AES-GCM key and nonce..."
    if warn_mode == WarnEnum.ALWAYS:
        logger.info(_message)
    elif warn_mode == WarnEnum.DEBUG:
        logger.debug(_message)

    _plaintext: str | bytes
    try:
        _aes_gcm = AESGCM(key=key)
        _plaintext = _aes_gcm.decrypt(nonce=nonce, data=ciphertext, associated_data=aad)

        _message = "Successfully decrypted ciphertext using AES-GCM key and nonce."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    except Exception:
        _message = "Failed to decrypt ciphertext using AES-GCM key and nonce!"
        if warn_mode == WarnEnum.ALWAYS:
            logger.error(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        raise

    if return_str:
        _plaintext = _plaintext.decode()

    return _plaintext


__all__ = [
    "gen_key",
    "encrypt",
    "decrypt",
]
