import os
import errno
import logging
from typing import cast

import aiofiles
import aiofiles.os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from pydantic import validate_call

from ...constants import WarnEnum
from ...io import async_remove_file, async_create_dir

from ._base import gen_key_pair

logger = logging.getLogger(__name__)


@validate_call
async def async_create_keys(
    asymmetric_keys_dir: str,
    key_size: int,
    private_key_fname: str,
    public_key_fname: str,
    force: bool = False,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> None:
    """Async generate and create asymmetric key files.

    Args:
        asymmetric_keys_dir (str     , required): Asymmetric keys directory.
        key_size            (int     , required): Asymmetric key size.
        private_key_fname   (str     , required): Asymmetric private key filename.
        public_key_fname    (str     , required): Asymmetric public key filename.
        force               (bool    , optional): Force to create asymmetric keys. Defaults to False.
        warn_mode           (WarnEnum, optional): Warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        FileExistsError: If warning mode is ERROR and asymmetric keys already exist.
        OSError        : If failed to create asymmetric keys.
    """

    _private_key_path = os.path.join(asymmetric_keys_dir, private_key_fname)
    _public_key_path = os.path.join(asymmetric_keys_dir, public_key_fname)

    if force:
        await async_remove_file(file_path=_private_key_path, warn_mode=warn_mode)
        await async_remove_file(file_path=_public_key_path, warn_mode=warn_mode)

    if (await aiofiles.os.path.isfile(_private_key_path)) and (
        await aiofiles.os.path.isfile(_public_key_path)
    ):
        logger.debug(
            f"Asymmetric keys already exist: ['{_private_key_path}', '{_public_key_path}']"
        )
        return

    _message = (
        f"Generating asymmetric keys: ['{_private_key_path}', '{_public_key_path}']..."
    )
    if warn_mode == WarnEnum.ALWAYS:
        logger.info(_message)
    elif warn_mode == WarnEnum.DEBUG:
        logger.debug(_message)

    _private_key: RSAPrivateKey
    _public_key: RSAPublicKey
    if await aiofiles.os.path.isfile(_private_key_path):
        if warn_mode == WarnEnum.ERROR:
            raise FileExistsError(f"'{_private_key_path}' private key already exists!")

        _private_key = cast(
            RSAPrivateKey,
            await async_get_private_key(private_key_path=_private_key_path),
        )

        _public_key: RSAPublicKey = _private_key.public_key()
    else:
        _key_pair = cast(
            tuple[RSAPrivateKey, RSAPublicKey], gen_key_pair(key_size=key_size)
        )
        _private_key, _public_key = _key_pair

    if await aiofiles.os.path.isfile(_public_key_path):
        if warn_mode == WarnEnum.ERROR:
            raise FileExistsError(f"'{_public_key_path}' public key already exists!")

        await async_remove_file(file_path=_public_key_path, warn_mode=warn_mode)

    _private_pem: bytes = _private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    _public_pem: bytes = _public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    await async_create_dir(create_dir=asymmetric_keys_dir, warn_mode=warn_mode)

    if not await aiofiles.os.path.isfile(_private_key_path):
        try:
            async with aiofiles.open(_private_key_path, "wb") as _private_key_file:
                await _private_key_file.write(_private_pem)

        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{_private_key_path}' private key already exists!")
            else:
                logger.error(f"Failed to create '{_private_key_path}' private key!")
                raise

    if not await aiofiles.os.path.isfile(_public_key_path):
        try:
            async with aiofiles.open(_public_key_path, "wb") as _public_key_file:
                await _public_key_file.write(_public_pem)

        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{_public_key_path}' public key already exists!")
            else:
                logger.error(f"Failed to create '{_public_key_path}' public key!")
                raise

    _message = f"Successfully generated asymmetric keys: ['{_private_key_path}', '{_public_key_path}']"
    if warn_mode == WarnEnum.ALWAYS:
        logger.info(_message)
    elif warn_mode == WarnEnum.DEBUG:
        logger.debug(_message)

    return


@validate_call
async def async_get_private_key(
    private_key_path: str, as_str: bool = False
) -> RSAPrivateKey | str:
    """Async read asymmetric private key from file.

    Args:
        private_key_path (str , required): Asymmetric private key path.
        as_str           (bool, optional): Return private key as string. Defaults to False.

    Raises:
        FileNotFoundError: If Asymmetric private key file not found.

    Returns:
        RSAPrivateKey | str: Asymmetric private key.
    """

    if not await aiofiles.os.path.isfile(private_key_path):
        raise FileNotFoundError(f"Not found '{private_key_path}' private key!")

    logger.debug(f"Reading '{private_key_path}' private key...")
    _private_key: RSAPrivateKey | str
    async with aiofiles.open(private_key_path, "rb") as _private_key_file:
        _private_key_bytes: bytes = await _private_key_file.read()
        _loaded_private_key = serialization.load_pem_private_key(
            data=_private_key_bytes, password=None
        )
        if not isinstance(_loaded_private_key, RSAPrivateKey):
            raise TypeError(
                f"`private_key_path` argument's file is not a valid private key {type(_loaded_private_key)} type, "
                "should be <RSAPrivateKey>!"
            )

        _private_key = _loaded_private_key

    if as_str:
        _private_key = _private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

    logger.debug(f"Successfully read '{private_key_path}' private key.")

    return _private_key


@validate_call
async def async_get_public_key(
    public_key_path: str, as_str: bool = False
) -> RSAPublicKey | str:
    """Async read asymmetric public key from file.

    Args:
        public_key_path (str , required): Asymmetric public key path.
        as_str          (bool, optional): Return public key as string. Defaults to False.

    Raises:
        FileNotFoundError: If asymmetric public key file not found.

    Returns:
        RSAPublicKey | str: Asymmetric public key.
    """

    if not await aiofiles.os.path.isfile(public_key_path):
        raise FileNotFoundError(f"Not found '{public_key_path}' public key!")

    logger.debug(f"Reading '{public_key_path}' public key...")
    _public_key: RSAPublicKey | str
    async with aiofiles.open(public_key_path, "rb") as _public_key_file:
        _public_key_bytes: bytes = await _public_key_file.read()
        _loaded_public_key = serialization.load_pem_public_key(data=_public_key_bytes)
        if not isinstance(_loaded_public_key, RSAPublicKey):
            raise TypeError(
                f"`public_key_path` argument's file is not a valid public key {type(_loaded_public_key)} type, "
                "should be <RSAPublicKey>!"
            )

        _public_key = _loaded_public_key

    if as_str:
        _public_key = _public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

    logger.debug(f"Successfully read '{public_key_path}' public key.")

    return _public_key


@validate_call
async def async_get_keys(
    private_key_path: str, public_key_path: str, as_str: bool = False
) -> tuple[RSAPrivateKey | str, RSAPublicKey | str]:
    """Async read asymmetric keys from file.

    Args:
        private_key_path (str , required): Asymmetric private key path.
        public_key_path  (str , required): Asymmetric public key path.
        as_str           (bool, optional): Return keys as strings. Defaults to False.

    Returns:
        tuple[RSAPrivateKey | str, RSAPublicKey | str]: Private and public keys.
    """

    _private_key = await async_get_private_key(
        private_key_path=private_key_path, as_str=as_str
    )
    _public_key = await async_get_public_key(
        public_key_path=public_key_path, as_str=as_str
    )

    return _private_key, _public_key


__all__ = [
    "async_create_keys",
    "async_get_private_key",
    "async_get_public_key",
    "async_get_keys",
]
