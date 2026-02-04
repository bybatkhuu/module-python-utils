# noqa: E402

import os
import sys
import json
import glob
import errno
import shutil
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
from pydantic import validate_call

from .._base import deep_merge
from ..constants import WarnEnum, HashAlgoEnum, ConfigFileFormatEnum, MAX_PATH_LENGTH


logger = logging.getLogger(__name__)


@validate_call
def create_dir(create_dir: str, warn_mode: WarnEnum | str = WarnEnum.DEBUG) -> None:
    """Create directory if `create_dir` doesn't exist.

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

    if not os.path.isdir(create_dir):
        try:
            _message = f"Creating '{create_dir}' directory..."
            if warn_mode == WarnEnum.ALWAYS:
                logger.info(_message)
            elif warn_mode == WarnEnum.DEBUG:
                logger.debug(_message)

            os.makedirs(create_dir)
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
def remove_dir(remove_dir: str, warn_mode: WarnEnum | str = WarnEnum.DEBUG) -> None:
    """Remove directory if `remove_dir` exists.

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

    if os.path.isdir(remove_dir):
        try:
            _message = f"Removing '{remove_dir}' directory..."
            if warn_mode == WarnEnum.ALWAYS:
                logger.info(_message)
            elif warn_mode == WarnEnum.DEBUG:
                logger.debug(_message)

            shutil.rmtree(remove_dir)
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
def remove_dirs(
    remove_dirs: list[str], warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Remove directories if `remove_dirs` exist.

    Args:
        remove_dirs (list[str]     , required): Remove directory paths as list.
        warn_mode   (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                Defaults to 'DEBUG'.
    """

    for _remove_dir in remove_dirs:
        remove_dir(remove_dir=_remove_dir, warn_mode=warn_mode)

    return


@validate_call
def remove_file(file_path: str, warn_mode: WarnEnum | str = WarnEnum.DEBUG) -> None:
    """Remove file if `file_path` exists.

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

    if os.path.isfile(file_path):
        try:
            _message = f"Removing '{file_path}' file..."
            if warn_mode == WarnEnum.ALWAYS:
                logger.info(_message)
            elif warn_mode == WarnEnum.DEBUG:
                logger.debug(_message)

            os.remove(file_path)
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
def remove_files(
    file_paths: list[str], warn_mode: WarnEnum | str = WarnEnum.DEBUG
) -> None:
    """Remove files if `file_paths` exist.

    Args:
        file_paths (list[str]     , required): Remove file paths as list.
        warn_mode  (WarnEnum | str, optional): Warning message mode, for example: 'ERROR', 'ALWAYS', 'DEBUG', 'IGNORE'.
                                                Defaults to 'DEBUG'.
    """

    for _file_path in file_paths:
        remove_file(file_path=_file_path, warn_mode=warn_mode)

    return


@validate_call
def get_file_checksum(
    file_path: str,
    hash_method: HashAlgoEnum = HashAlgoEnum.md5,
    chunk_size: int = 4096,
    warn_mode: WarnEnum | str = WarnEnum.DEBUG,
) -> str | None:
    """Get file checksum.

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
    if os.path.isfile(file_path):
        _file_hash = hashlib.new(hash_method.value)
        with open(file_path, "rb") as _file:
            while True:
                _file_chunk = _file.read(chunk_size)
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
def read_yaml_file(file_path: str | Path) -> dict[str, Any]:
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

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' YAML file!")

    try:
        with open(file_path, encoding="utf-8") as _file:
            _data = yaml.safe_load(_file) or {}
    except Exception:
        logger.error(f"Failed to read '{file_path}' YAML file!")
        raise

    return _data


@validate_call
def read_json_file(file_path: str | Path) -> dict[str, Any]:
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

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' JSON file!")

    try:
        with open(file_path, encoding="utf-8") as _file:
            _data = json.load(_file) or {}
    except Exception:
        logger.error(f"Failed to read '{file_path}' JSON file!")
        raise

    return _data


@validate_call
def read_toml_file(file_path: str | Path) -> dict[str, Any]:
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

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' TOML file!")

    try:
        if _binary_toml:
            with open(file_path, "rb") as _file:
                _data = tomllib.load(_file) or {}  # type: ignore
        else:
            with open(file_path, encoding="utf-8") as _file:
                _data = tomllib.load(_file) or {}  # type: ignore
    except Exception:
        logger.error(f"Failed to read '{file_path}' TOML file!")
        raise

    return _data


@validate_call
def read_ini_file(file_path: str | Path) -> dict[str, Any]:
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

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Not found '{file_path}' INI config file!")

    try:
        _config_parser = configparser.ConfigParser()
        _config_parser.read(file_path)
        for _section in _config_parser.sections():
            _config[_section] = dict(_config_parser.items(_section))

    except Exception:
        logger.error(f"Failed to read '{file_path}' INI config file!")
        raise

    return _config


@validate_call
def read_config_file(config_path: str | Path) -> dict[str, Any]:
    """Read config file (YAML, JSON, TOML, INI).

    Args:
        config_path (str | Path, required): Config file path.

    Raises:
        FileNotFoundError: If config file is not found.
        ValueError       : If config file format is not supported.

    Returns:
        dict[str, Any]: Config file data as dictionary.
    """

    _config: dict[str, Any] = {}

    if isinstance(config_path, str):
        config_path = Path(config_path)

    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Not found '{config_path}' config file!")

    _suffix = config_path.suffix.lower()
    if _suffix in (".yaml", ".yml"):
        _config = read_yaml_file(file_path=config_path)
    elif _suffix == ".json":
        _config = read_json_file(file_path=config_path)
    elif _suffix == ".toml":
        _config = read_toml_file(file_path=config_path)
    elif _suffix in (".ini", ".cfg"):
        _config = read_ini_file(file_path=config_path)
    else:
        raise ValueError(
            f"Unsupported config file format '{config_path.suffix}' for '{config_path}'!"
        )

    return _config


@validate_call
def read_all_configs(
    configs_dir: str | Path | list[str | Path],
    allowed_formats: list[ConfigFileFormatEnum] = [
        ConfigFileFormatEnum.YAML,
        ConfigFileFormatEnum.JSON,
        ConfigFileFormatEnum.TOML,
    ],
) -> dict[str, Any]:
    """Read all config files from directory or directories and merge them.

    Args:
        configs_dir     (str | Path | list[str | Path], required): Configs directory or directories.
        allowed_formats (list[ConfigFileFormatEnum]   , optional): Allowed config file formats to read.
                                                                    Defaults to [YAML, JSON, TOML].

    Returns:
        dict[str, Any]: Dictionary containing all merged config data from all files.
    """

    _config_dict: dict[str, Any] = {}

    if not isinstance(configs_dir, list):
        configs_dir = [configs_dir]

    _file_paths: list[str] = []
    for _config_dir in configs_dir:
        if isinstance(_config_dir, str):
            _config_dir = Path(_config_dir)

        if not os.path.isabs(_config_dir):
            _current_dir = os.getcwd()
            _config_dir = os.path.join(_current_dir, _config_dir)

        if os.path.isdir(_config_dir):
            if ConfigFileFormatEnum.YAML in allowed_formats:
                _file_paths.extend(glob.glob(os.path.join(_config_dir, "*.yaml")))
                _file_paths.extend(glob.glob(os.path.join(_config_dir, "*.yml")))

            if ConfigFileFormatEnum.JSON in allowed_formats:
                _file_paths.extend(glob.glob(os.path.join(_config_dir, "*.json")))

            if ConfigFileFormatEnum.TOML in allowed_formats:
                _file_paths.extend(glob.glob(os.path.join(_config_dir, "*.toml")))

            if ConfigFileFormatEnum.INI in allowed_formats:
                _file_paths.extend(glob.glob(os.path.join(_config_dir, "*.ini")))
                _file_paths.extend(glob.glob(os.path.join(_config_dir, "*.cfg")))

    _file_paths.sort()
    for _file_path in _file_paths:
        _config_data = read_config_file(config_path=_file_path)
        _config_dict = deep_merge(_config_dict, _config_data)

    return _config_dict


__all__ = [
    "create_dir",
    "remove_dir",
    "remove_dirs",
    "remove_file",
    "remove_files",
    "get_file_checksum",
    "read_yaml_file",
    "read_json_file",
    "read_toml_file",
    "read_ini_file",
    "read_config_file",
    "read_all_configs",
]
