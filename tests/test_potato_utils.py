import logging

# import pytest

# try:
#     from potato_util import io as io_utils
# except ImportError:
#     from potato_util import io as io_utils


logger = logging.getLogger(__name__)


def test_init():
    logger.info("Testing initialization of 'potato_util'...")

    logger.info("Done: Initialization of 'potato_util'.\n")
