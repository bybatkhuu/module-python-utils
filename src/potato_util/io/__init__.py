# flake8: noqa

import importlib.util

from ._sync import *

if (importlib.util.find_spec("aiofiles") is not None) and (
    importlib.util.find_spec("aioshutil") is not None
):
    from ._async import *
