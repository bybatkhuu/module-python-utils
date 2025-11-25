import sys
import json
import errno
import hashlib
import logging
import configparser
from pathlib import Path
from typing import Any

_binary_toml = False
if sys.version_info >= (3, 11):
    import tomllib  # type: ignore

    _binary_toml = True
else:
    import toml as tomllib  # type: ignore

import yaml
import aioshutil
import aiofiles.os
from pydantic import validate_call

from ..constants import WarnEnum, HashAlgoEnum, MAX_PATH_LENGTH


logger = logging.getLogger(__name__)


@validate_call
async def async_create_dir(
    create_dir: str, warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Asynchronous create directory if `create_dir` doesn't exist.

    Args:
        create_dir (str           , required): Create directory path.
        warn_mode  (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                Defaults to 'DEBUG'.

    Raises:
        ValueError: If `create_dir` argument length is out of range.
        OSError   : When warning mode is set to ERROR and directory already exists.
        OSError   : If failed to create directory.
    """

    create_dir = create_dir.strip()
    if (len(create_dir) < 1) or (MAX_PATH_LENGTH < len(create_dir)):
        raise ValueError(
            f"`create_dir` argument length {len(create_dir)} is out of range, "
            f"must be between 1 and {MAX_PATH_LENGTH} characters!"
        )

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    if not await aiofiles.os.path.isdir(create_dir):
        try:
            _message = f"Creating '{create_dir}' directory..."
            if warn_mode == WarnEnum.ALWAYS:
                logger.info(_message)
            elif warn_mode == WarnEnum.DEBUG:
                logger.debug(_message)

            await aiofiles.os.makedirs(create_dir)
        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{create_dir}' directory already exists!")
            else:
                logger.error(f"Failed to create '{create_dir}' directory!")
                raise

        _message = f"Successfully created '{create_dir}' directory."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    elif warn_mode == WarnEnum.ERROR:
        raise OSError(errno.EEXIST, f"'{create_dir}' directory already exists!")

    return


@validate_call
async def async_remove_dir(
    remove_dir: str, warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Asynchronous remove directory if `remove_dir` exists.

    Args:
        remove_dir (str           , required): Remove directory path.
        warn_mode  (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                Defaults to 'DEBUG'.

    Raises:
        ValueError: If `remove_dir` argument length is out of range.
        OSError   : When warning mode is set to ERROR and directory doesn't exist.
        OSError   : If failed to remove directory.
    """

    remove_dir = remove_dir.strip()
    if (len(remove_dir) < 1) or (MAX_PATH_LENGTH < len(remove_dir)):
        raise ValueError(
            f"`remove_dir` argument length {len(remove_dir)} is out of range, "
            f"must be between 1 and {MAX_PATH_LENGTH} characters!"
        )

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    if await aiofiles.os.path.isdir(remove_dir):
        try:
            _message = f"Removing '{remove_dir}' directory..."
            if warn_mode == WarnEnum.ALWAYS:
                logger.info(_message)
            elif warn_mode == WarnEnum.DEBUG:
                logger.debug(_message)

            await aioshutil.rmtree(remove_dir)
        except OSError as err:
            if (err.errno == errno.ENOENT) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{remove_dir}' directory doesn't exist!")
            else:
                logger.error(f"Failed to remove '{remove_dir}' directory!")
                raise

        _message = f"Successfully removed '{remove_dir}' directory."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    elif warn_mode == WarnEnum.ERROR:
        raise OSError(errno.ENOENT, f"'{remove_dir}' directory doesn't exist!")

    return


@validate_call
async def async_remove_dirs(
    remove_dirs: list[str], warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Asynchronous remove directories if `remove_dirs` exists.

    Args:
        remove_dirs (list[str]     , required): Remove directories paths as list.
        warn_mode   (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                    Defaults to 'DEBUG'.
    """

    for _remove_dir in remove_dirs:
        await async_remove_dir(remove_dir=_remove_dir, warn_mode=warn_mode)

    return


@validate_call
async def async_remove_file(
    file_path: str, warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Asynchronous remove file if `file_path` exists.

    Args:
        file_path (str           , required): Remove file path.
        warn_mode (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                Defaults to 'DEBUG'.

    Raises:
        ValueError: If `file_path` argument length is out of range.
        OSError   : When warning mode is set to ERROR and file doesn't exist.
        OSError   : If failed to remove file.
    """

    file_path = file_path.strip()
    if (len(file_path) < 1) or (MAX_PATH_LENGTH < len(file_path)):
        raise ValueError(
            f"`file_path` argument length {len(file_path)} is out of range, "
            f"must be between 1 and {MAX_PATH_LENGTH} characters!"
        )

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    if await aiofiles.os.path.isfile(file_path):
        try:
            _message = f"Removing '{file_path}' file..."
            if warn_mode == WarnEnum.ALWAYS:
                logger.info(_message)
            elif warn_mode == WarnEnum.DEBUG:
                logger.debug(_message)

            await aiofiles.os.remove(file_path)
        except OSError as err:
            if (err.errno == errno.ENOENT) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{file_path}' file doesn't exist!")
            else:
                logger.error(f"Failed to remove '{file_path}' file!")
                raise

        _message = f"Successfully removed '{file_path}' file."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    elif warn_mode == WarnEnum.ERROR:
        raise OSError(errno.ENOENT, f"'{file_path}' file doesn't exist!")

    return


@validate_call
async def async_remove_files(
    file_paths: list[str], warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Asynchronous remove files if `file_paths` exists.

    Args:
        file_paths (list[str]     , required): Remove file paths as list.
        warn_mode  (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                Defaults to 'DEBUG'.
    """

    for _file_path in file_paths:
        await async_remove_file(file_path=_file_path, warn_mode=warn_mode)

    return


@validate_call
async def async_get_file_checksum(
    file_path: str,
    hash_method: HashAlgoEnum = HashAlgoEnum.md5,
    chunk_size: int = 4096,
    warn_mode: WarnEnum | str = WarnEnum.DEBUG,
) -> str | None:
    """Asynchronous get file checksum.

    Args:
        file_path   (str           , required): Target file path.
        hash_method (HashAlgoEnum  , optional): Hash method. Defaults to `HashAlgoEnum.md5`.
        chunk_size  (int           , optional): Chunk size. Defaults to 4096.
        warn_mode   (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                    Defaults to 'DEBUG'.

    Raises:
        ValueError: If `file_path` argument length is out of range.
        ValueError: If `chunk_size` argument value is invalid.
        OSError   : When warning mode is set to ERROR and file doesn't exist.

    Returns:
        str | None: File checksum or None if file doesn't exist.
    """

    file_path = file_path.strip()
    if (len(file_path) < 1) or (MAX_PATH_LENGTH < len(file_path)):
        raise ValueError(
            f"`file_path` argument length {len(file_path)} is out of range, "
            f"must be between 1 and {MAX_PATH_LENGTH} characters!"
        )

    if chunk_size < 10:
        raise ValueError(
            f"`chunk_size` argument value {chunk_size} is invalid, must be greater than 10!"
        )

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    _file_checksum: str | None = None
    if await aiofiles.os.path.isfile(file_path):
        _file_hash = hashlib.new(hash_method.value)
        async with aiofiles.open(file_path, "rb") as _file:
            while True:
                _file_chunk = await _file.read(chunk_size)
                if not _file_chunk:
                    break
                _file_hash.update(_file_chunk)

        _file_checksum = _file_hash.hexdigest()
    else:
        _message = f"'{file_path}' file doesn't exist!"
        if warn_mode == WarnEnum.ALWAYS:
            logger.warning(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)
        elif warn_mode == WarnEnum.ERROR:
            raise OSError(errno.ENOENT, _message)

    return _file_checksum


@validate_call
async def async_read_yaml_file(file_path: str | Path) -> dict[str, Any]:
    """Read YAML file.

    Args:
        file_path (str | Path, required): YAML file path.

    Raises:
        FileNotFoundError: If YAML file is not found.
        Exception        : If failed to read YAML file.

    Returns:
        dict[str, Any]: YAML file data as dictionary.
    """

    _data: dict[str, Any] = {}

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not await aiofiles.os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' YAML file!")

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as _file:
            _content = await _file.read()
            _data = yaml.safe_load(_content) or {}
    except Exception:
        logger.error(f"Failed to read '{file_path}' YAML file!")
        raise

    return _data


@validate_call
async def async_read_json_file(file_path: str | Path) -> dict[str, Any]:
    """Read JSON file.

    Args:
        file_path (str | Path, required): JSON file path.

    Raises:
        FileNotFoundError: If JSON file is not found.
        Exception        : If failed to read JSON file.

    Returns:
        dict[str, Any]: JSON file data as dictionary.
    """

    _data: dict[str, Any] = {}

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not await aiofiles.os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' JSON file!")

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as _file:
            _content = await _file.read()
            _data = json.loads(_content) or {}
    except Exception:
        logger.error(f"Failed to read '{file_path}' JSON file!")
        raise

    return _data


@validate_call
async def async_read_toml_file(file_path: str | Path) -> dict[str, Any]:
    """Read TOML file.

    Args:
        file_path (str | Path, required): TOML file path.

    Raises:
        FileNotFoundError: If TOML file is not found.
        Exception        : If failed to read TOML file.

    Returns:
        dict[str, Any]: TOML file data as dictionary.
    """

    _data: dict[str, Any] = {}

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not await aiofiles.os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' TOML file!")

    try:
        _content: str = ""
        if _binary_toml:
            async with aiofiles.open(file_path, "rb") as _file:
                _content = await _file.read()  # type: ignore
        else:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as _file:
                _content = await _file.read()  # type: ignore

        _data = tomllib.loads(_content) or {}
    except Exception:
        logger.error(f"Failed to read '{file_path}' TOML file!")
        raise

    return _data


@validate_call
async def async_read_ini_file(file_path: str | Path) -> dict[str, Any]:
    """Read INI config file.

    Args:
        file_path (str | Path, required): INI config file path.

    Raises:
        FileNotFoundError: If INI config file is not found.
        Exception        : If failed to read INI config file.

    Returns:
        dict[str, Any]: INI config file data as dictionary.
    """

    _config: dict[str, Any] = {}

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not await aiofiles.os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' INI config file!")

    try:
        _content: str = ""
        async with aiofiles.open(file_path, "r", encoding="utf-8") as _file:
            _content = await _file.read()

        _config_parser = configparser.ConfigParser()
        _config_parser.read_string(_content)
        for _section in _config_parser.sections():
            _config[_section] = dict(_config_parser.items(_section))

    except Exception:
        logger.error(f"Failed to read '{file_path}' INI config file!")
        raise

    return _config


@validate_call
async def async_read_config_file(config_path: str | Path) -> dict[str, Any]:

    _config: dict[str, str] = {}

    if isinstance(config_path, str):
        config_path = Path(config_path)

    if not await aiofiles.os.path.isfile(config_path):
        raise FileNotFoundError(f"Not found '{config_path}' config file!")

    _suffix = config_path.suffix.lower()
    if _suffix in (".yaml", ".yml"):
        _config = await async_read_yaml_file(config_path)
    elif _suffix == ".json":
        _config = await async_read_json_file(config_path)
    elif _suffix == ".toml":
        _config = await async_read_toml_file(config_path)
    elif _suffix in (".ini", ".cfg"):
        _config = await async_read_ini_file(config_path)
    else:
        raise ValueError(
            f"Unsupported config file format '{_suffix}' for '{config_path}'!"
        )

    return _config


__all__ = [
    "async_create_dir",
    "async_remove_dir",
    "async_remove_dirs",
    "async_remove_file",
    "async_remove_files",
    "async_get_file_checksum",
    "async_read_yaml_file",
    "async_read_json_file",
    "async_read_toml_file",
    "async_read_ini_file",
    "async_read_config_file",
]
