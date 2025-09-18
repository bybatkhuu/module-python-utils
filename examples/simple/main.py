#!/usr/bin/env python

# Standard libraries
import sys
import logging

# Internal modules
# from potato_utils import io as io_utils


logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S %z",
        format="[%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d]: %(message)s",
    )

    logger.info("Done!\n")
    return


if __name__ == "__main__":
    main()
