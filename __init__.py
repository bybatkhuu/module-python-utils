# flake8: noqa

try:
    from .src.potato_util import *
except ImportError:
    from src.potato_util import *
