#!/usr/bin/env python

# Standard libraries
import os
import sys
import logging

# Internal modules
from potato_util import http as http_utils
from potato_util import io as io_utils


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

    _http_status_result = http_utils.get_http_status(status_code=403)
    logger.info(f"HTTP status and known: {_http_status_result}")

    _url = "https://www.google.com"
    _is_connectable = http_utils.is_connectable(url=_url, timeout=3, check_status=True)  # type: ignore
    logger.info(f"Is '{_url}' connectable: {_is_connectable}")

    io_utils.create_dir(create_dir="./some_dir", warn_mode="ALWAYS")  # type: ignore
    io_utils.remove_dir(remove_dir="./some_dir", warn_mode="ALWAYS")  # type: ignore

    return


if __name__ == "__main__":
    main()
