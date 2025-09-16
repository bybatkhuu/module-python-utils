# flake8: noqa

try:
    from .src.potato_utils import *
except ImportError:
    from src.potato_utils import *
