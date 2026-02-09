#!/usr/bin/env python

# Standard libraries
import os
import sys
import logging

# Third-party libraries
from pydantic import AnyHttpUrl

# Internal modules
import potato_util
import potato_util.dt as dt_utils
import potato_util.generator as gen_utils
import potato_util.sanitizer as sanitizer_utils
import potato_util.secure as secure_utils
import potato_util.validator as validator_utils
import potato_util.http as http_utils

logger = logging.getLogger(__name__)


def main() -> None:
    _log_level = logging.INFO
    if str(os.getenv("DEBUG", "0")).lower() in ("1", "true", "t", "yes", "y"):
        _log_level = logging.DEBUG

    logging.basicConfig(
        stream=sys.stdout,
        level=_log_level,
        datefmt="%Y-%m-%d %H:%M:%S %z",
        format="[%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d]: %(message)s",
    )

    # Base utils:
    logger.info("[BASE UTILITIES]")
    _dict1 = {"a": 1, "b": {"c": 2, "d": 3}, "g": [2, 3, 4]}
    _dict2 = {"b": {"c": 20, "e": 30}, "f": 40, "g": [5, 6, 7]}
    _merged_dict = potato_util.deep_merge(_dict1, _dict2)
    logger.info(f"Merged dict: {_merged_dict}")

    _camel_str = "CamelCaseString"
    _snake_str = potato_util.camel_to_snake(_camel_str)
    logger.info(f"Converted '{_camel_str}' to '{_snake_str}'")
    logger.info("-" * 80)

    # Datetime utils:
    logger.info("[DATETIME UTILITIES]")
    _now_local_dt = dt_utils.now_local_dt()
    logger.info(f"Current local datetime: {_now_local_dt}")

    _now_utc_dt = dt_utils.now_utc_dt()
    logger.info(f"Current UTC datetime: {_now_utc_dt}")

    _now_ny_dt = dt_utils.now_dt(tz="America/New_York")
    logger.info(f"Current New York datetime: {_now_ny_dt}")

    _now_ts = dt_utils.now_ts()
    logger.info(f"Current UTC timestamp (seconds): {_now_ts}")

    _now_ts_ms = dt_utils.now_ts(unit="MILLISECONDS")
    logger.info(f"Current UTC timestamp (ms): {_now_ts_ms}")

    _now_ts_micro = dt_utils.now_ts(unit="MICROSECONDS")
    logger.info(f"Current UTC timestamp (microseconds): {_now_ts_micro}")

    _now_ts_ns = dt_utils.now_ts(unit="NANOSECONDS")
    logger.info(f"Current UTC timestamp (nanoseconds): {_now_ts_ns}")

    _dt_ts = dt_utils.dt_to_ts(dt=_now_local_dt)
    logger.info(f"Converted local datetime to UTC timestamp (seconds): {_dt_ts}")

    _replaced_tz_dt = dt_utils.replace_tz(dt=_now_local_dt, tz="Asia/Ulaanbaatar")
    logger.info(f"Add or replace timezone with Asia/Ulaanbaatar: {_replaced_tz_dt}")

    _converted_dt = dt_utils.convert_tz(dt=_now_ny_dt, tz="Asia/Seoul")
    logger.info(
        f"Calculated and converted timezone from New York to Seoul: {_converted_dt}"
    )

    _dt_iso = dt_utils.dt_to_iso(dt=_now_local_dt)
    logger.info(f"Parsing datetime to ISO 8601 format string: {_dt_iso}")

    _future_dt = dt_utils.calc_future_dt(delta=3600, dt=_now_local_dt, tz="Asia/Tokyo")
    logger.info(f"Calculated future datetime after 3600 seconds in Tokyo: {_future_dt}")
    logger.info("-" * 80)

    # Generator utils:
    logger.info("[GENERATOR UTILITIES]")
    _unique_id = gen_utils.gen_unique_id(prefix="item_")
    logger.info(f"Generated unique ID based on datetime and UUIDv4: {_unique_id}")

    _random_str = gen_utils.gen_random_string(length=32, is_alphanum=False)
    logger.info(f"Generated secure random string: {_random_str}")
    logger.info("-" * 80)

    # Sanitizer utils:
    logger.info("[SANITIZER UTILITIES]")
    _raw_html = '  <script>alert("XSS Attack!");</script>  '
    _escaped_html = sanitizer_utils.escape_html(val=_raw_html)
    logger.info(f"Escaped HTML: {_escaped_html}")

    _raw_url = "https://www.example.com/search?q=potato util&body=<script>alert('Attack!')</script>&lang=한국어"
    _escaped_url = sanitizer_utils.escape_url(val=_raw_url)
    logger.info(f"Escaped URL: {_escaped_url}")

    _raw_str = "Hello@World! This is a test_string with special#chars$%&*()[]{};:'\",.<>?/\\|`~"
    _sanitized_str = sanitizer_utils.sanitize_special_chars(val=_raw_str, mode="STRICT")
    logger.info(f"Sanitized string: {_sanitized_str}")
    logger.info("-" * 80)

    # Secure utils:
    logger.info("[SECURE UTILITIES]")
    _input_str = "SensitiveInformation123!"
    _hashed_str_sha256 = secure_utils.hash_str(val=_input_str, algorithm="sha256")
    logger.info(f"SHA-256 hashed string: {_hashed_str_sha256}")
    logger.info("-" * 80)

    # Validator utils:
    logger.info("[VALIDATOR UTILITIES]")
    _is_yes_truthy = validator_utils.is_truthy(val="Yes")
    logger.info(f"Is 'Yes' truthy: {_is_yes_truthy}")
    _is_off_truthy = validator_utils.is_truthy(val="OFF")
    logger.info(f"Is 'OFF' truthy: {_is_off_truthy}")

    _is_no_falsy = validator_utils.is_falsy(val="f")
    logger.info(f"Is 'f' falsy: {_is_no_falsy}")
    _is_1_falsy = validator_utils.is_falsy(val="1")
    logger.info(f"Is '1' falsy: {_is_1_falsy}")

    _request_id = "f058ebd6-02f7-4d3f-942e-904344e8cde5"
    _is_valid_request_id = validator_utils.is_request_id(val=_request_id)
    logger.info(f"Is '{_request_id}' a valid request ID: {_is_valid_request_id}")

    _blacklist = ["hacker", "guest"]
    _input_username = "hacker"
    _is_blacklisted = validator_utils.is_blacklisted(
        val=_input_username, blacklist=_blacklist
    )
    logger.info(f"Is '{_input_username}' blacklisted: {_is_blacklisted}")

    _pattern = r"^[a-zA-Z0-9_]{3,16}$"  # Alphanumeric and underscores, 3-16 chars
    _test_username = "valid_user123"
    _is_valid_username = validator_utils.is_valid(val=_test_username, pattern=_pattern)
    logger.info(f"Is '{_test_username}' a valid username: {_is_valid_username}")

    _string_with_special_chars = "Hello@World!"
    _has_special_chars = validator_utils.has_special_chars(
        val=_string_with_special_chars, mode="STRICT"
    )
    logger.info(
        f"Does '{_string_with_special_chars}' have special chars: {_has_special_chars}"
    )
    logger.info("-" * 80)

    # HTTP utils:
    logger.info("[HTTP UTILITIES]")
    _http_status_tuple = http_utils.get_http_status(status_code=403)
    logger.info(f"HTTP status and known: {_http_status_tuple}")

    _url = AnyHttpUrl("https://www.google.com")
    _is_connectable = http_utils.is_connectable(url=_url, timeout=3, check_status=True)
    logger.info(f"Is '{_url}' connectable: {_is_connectable}")
    logger.info("-" * 80)

    return


if __name__ == "__main__":
    main()
