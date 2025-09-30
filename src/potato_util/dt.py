import time
import logging
from zoneinfo import ZoneInfo
from datetime import datetime, timezone, tzinfo, timedelta

from pydantic import validate_call

from .constants import WarnEnum, TSUnitEnum


logger = logging.getLogger(__name__)


def now_local_dt() -> datetime:
    """Get current datetime in local timezone with tzinfo.

    Returns:
        datetime: Current datetime in local timezone with tzinfo.
    """

    _local_dt = datetime.now().astimezone()
    return _local_dt


def now_utc_dt() -> datetime:
    """Get current datetime in UTC timezone with tzinfo.

    Returns:
        datetime: Current datetime in UTC timezone with tzinfo.
    """

    _utc_dt = datetime.now(tz=timezone.utc)
    return _utc_dt


@validate_call(config={"arbitrary_types_allowed": True})
def now_dt(tz: ZoneInfo | tzinfo | str | None = None) -> datetime:
    """Get current datetime in specified timezone with tzinfo.

    Args:
        tz (ZoneInfo | tzinfo | str | None, optional): Timezone info. Defaults to None (UTC timezone).

    Returns:
        datetime: Current datetime in specified timezone with tzinfo.
    """

    _dt = now_utc_dt()
    if tz:
        _dt = convert_tz(dt=_dt, tz=tz)
    return _dt


@validate_call(config={"arbitrary_types_allowed": True})
def replace_tz(dt: datetime, tz: ZoneInfo | tzinfo | str) -> datetime:
    """Add or replace timezone info to datetime object.

    Args:
        dt (datetime               , required): Datetime object.
        tz (ZoneInfo | tzinfo | str, required): Timezone info.

    Raises:
        ZoneInfoNotFoundError: If `tz` argument value is invalid.

    Returns:
        datetime: Datetime object with timezone info.
    """

    if isinstance(tz, str):
        tz = ZoneInfo(tz)

    dt = dt.replace(tzinfo=tz)
    return dt


@validate_call(config={"arbitrary_types_allowed": True})
def convert_tz(
    dt: datetime,
    tz: ZoneInfo | tzinfo | str,
    warn_mode: WarnEnum | str = WarnEnum.ALWAYS,
) -> datetime:
    """Convert datetime object to another timezone.

    Args:
        dt        (datetime               , required): Datetime object to convert.
        tz        (ZoneInfo | tzinfo | str, required): Timezone info to convert.
        warn_mode (WarnEnum | str         , optional): Warning mode. Defaults to WarnEnum.ALWAYS.

    Raises:
        ValueError: If `dt` argument doesn't have any timezone info and `warn_mode` is set to WarnEnum.ERROR.
        ValueError: If `warn_mode` argument value is invalid.

    Returns:
        datetime: Datetime object which has been converted to another timezone.
    """

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    if not dt.tzinfo:
        _message = "Not found any timezone info in `dt` argument, assuming it's UTC timezone..."
        if warn_mode == WarnEnum.ALWAYS:
            logger.warning(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)
        elif warn_mode == WarnEnum.ERROR:
            _message = "Not found any timezone info in `dt` argument!"
            logger.error(_message)
            raise ValueError(_message)

        dt = replace_tz(dt=dt, tz="UTC")

    if isinstance(tz, str):
        tz = ZoneInfo(tz)

    dt = dt.astimezone(tz=tz)
    return dt


@validate_call
def dt_to_iso(
    dt: datetime, sep: str = "T", warn_mode: WarnEnum | str = WarnEnum.IGNORE
) -> str:
    """Convert datetime object to ISO 8601 format.

    Args:
        dt        (datetime      , required): Datetime object.
        sep       (str           , optional): Separator between date and time. Defaults to "T".
        warn_mode (WarnEnum | str, optional): Warning mode. Defaults to WarnEnum.IGNORE.

    Raises:
        ValueError: If `dt` argument doesn't have any timezone info and `warn_mode` is set to WarnEnum.ERROR.
        ValueError: If `sep` argument length is greater than 8.
        ValueError: If `warn_mode` argument value is invalid.

    Returns:
        str: Datetime string in ISO 8601 format.
    """

    sep = sep.strip()
    if 8 < len(sep):
        raise ValueError(
            f"`sep` argument length '{len(sep)}' is too long, must be less than or equal to 8!"
        )

    if isinstance(warn_mode, str):
        warn_mode = WarnEnum(warn_mode.strip().upper())

    if not dt.tzinfo:
        _message = "Not found any timezone info in `dt` argument, assuming it's UTC timezone..."
        if warn_mode == WarnEnum.ALWAYS:
            logger.warning(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)
        elif warn_mode == WarnEnum.ERROR:
            _message = "Not found any timezone info in `dt` argument!"
            logger.error(_message)
            raise ValueError(_message)

        dt = replace_tz(dt=dt, tz="UTC")

    _dt_str = dt.isoformat(sep=sep, timespec="milliseconds")
    return _dt_str


@validate_call(config={"arbitrary_types_allowed": True})
def calc_future_dt(
    delta: timedelta | int,
    dt: datetime | None = None,
    tz: ZoneInfo | tzinfo | str | None = None,
) -> datetime:
    """Calculate future datetime by adding delta time to current or specified datetime.

    Args:
        delta (timedelta | int             , required): Delta time to add to current or specified datetime.
        dt    (datetime | None             , optional): Datetime before adding delta time. Defaults to None.
        tz    (ZoneInfo | tzinfo, str, None, optional): Timezone info. Defaults to None.

    Returns:
        datetime: Calculated future datetime.
    """

    if not dt:
        dt = now_utc_dt()

    if tz:
        dt = convert_tz(dt=dt, tz=tz)

    if isinstance(delta, int):
        delta = timedelta(seconds=delta)

    _future_dt = dt + delta
    return _future_dt


@validate_call
def now_ts(unit: TSUnitEnum | str = TSUnitEnum.SECONDS) -> int:
    """Get current timestamp in UTC timezone.

    Args:
        unit (TSUnitEnum | str, optional): Type of timestamp unit. Defaults to TSUnitEnum.SECONDS.

    Raises:
        ValueError: If `unit` argument value is invalid.

    Returns:
        int: Current timestamp.
    """

    _now_ts: int
    if unit == TSUnitEnum.SECONDS:
        _now_ts = int(time.time())
    elif unit == TSUnitEnum.MILLISECONDS:
        _now_ts = int(time.time() * 1000)
    elif unit == TSUnitEnum.MICROSECONDS:
        _now_ts = int(time.time_ns() / 1000)
    elif unit == TSUnitEnum.NANOSECONDS:
        _now_ts = int(time.time_ns())
    else:
        raise ValueError(f"`unit` argument value '{unit}' is invalid!")

    return _now_ts


@validate_call
def dt_to_ts(dt: datetime, unit: TSUnitEnum | str = TSUnitEnum.SECONDS) -> int:
    """Convert datetime to timestamp.

    Args:
        dt   (datetime        , required): Datetime object to convert.
        unit (TSUnitEnum | str, optional): Type of timestamp unit. Defaults to `TSUnitEnum.SECONDS`.

    Raises:
        ValueError: If `unit` argument value is invalid.

    Returns:
        int: Converted timestamp.
    """

    _ts: int
    if unit == TSUnitEnum.SECONDS:
        _ts = int(dt.timestamp())
    elif unit == TSUnitEnum.MILLISECONDS:
        _ts = int(dt.timestamp() * 1000)
    elif unit == TSUnitEnum.MICROSECONDS:
        _ts = int(dt.timestamp() * 1000000)
    elif unit == TSUnitEnum.NANOSECONDS:
        _ts = int(dt.timestamp() * 1000000000)
    else:
        raise ValueError(f"`unit` argument value '{unit}' is invalid!")

    return _ts


__all__ = [
    "now_utc_dt",
    "now_local_dt",
    "now_dt",
    "replace_tz",
    "convert_tz",
    "dt_to_iso",
    "calc_future_dt",
    "now_ts",
    "dt_to_ts",
]
