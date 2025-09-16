import logging

# import pytest

# try:
#     from potato_utils import io as io_utils
# except ImportError:
#     from potato_utils import io as io_utils


logger = logging.getLogger(__name__)


def test_init(my_object):
    logger.info("Testing initialization of 'potato_utils'...")

    logger.info("Done: Initialization of 'potato_utils'.\n")
