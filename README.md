# Potato Util (Python Utils)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bybatkhuu/module-python-utils/2.build-publish.yml?logo=GitHub)](https://github.com/bybatkhuu/module-python-utils/actions/workflows/2.build-publish.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/bybatkhuu/module-python-utils?logo=GitHub&color=blue)](https://github.com/bybatkhuu/module-python-utils/releases)

'potato_util' is collection of simple useful utils package for python.

## ✨ Features

- Python utilities
- Datetime utilities
- Generator utilities
- Sanitation utilities
- Security utilities
- Validation utilities
- HTTP utilities
- File I/O utilities
- And more...

---

## 🛠 Installation

### 1. 🚧 Prerequisites

- Install **Python (>= v3.10)** and **pip (>= 23)**:
    - **[RECOMMENDED] [Miniconda (v3)](https://www.anaconda.com/docs/getting-started/miniconda/install)**
    - *[arm64/aarch64] [Miniforge (v3)](https://github.com/conda-forge/miniforge)*
    - *[Python virutal environment] [venv](https://docs.python.org/3/library/venv.html)*

[OPTIONAL] For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) ([video tutorial](https://www.youtube.com/watch?v=snCP3c7wXw0))

### 2. 📥 Download or clone the repository

[TIP] Skip this step, if you're going to install the package directly from **PyPi** or **GitHub** repository.

**2.1.** Prepare projects directory (if not exists):

```sh
# Create projects directory:
mkdir -pv ~/workspaces/projects

# Enter into projects directory:
cd ~/workspaces/projects
```

**2.2.** Follow one of the below options **[A]**, **[B]** or **[C]**:

**OPTION A.** Clone the repository:

```sh
git clone https://github.com/bybatkhuu/module-python-utils.git && \
    cd module-python-utils
```

**OPTION B.** Clone the repository (for **DEVELOPMENT**: git + ssh key):

```sh
git clone git@github.com:bybatkhuu/module-python-utils.git && \
    cd module-python-utils
```

**OPTION C.** Download source code:

1. Download archived **zip** file from [**releases**](https://github.com/bybatkhuu/module-python-utils/releases).
2. Extract it into the projects directory.

### 3. 📦 Install the package

[NOTE] Choose one of the following methods to install the package **[A ~ F]**:

**OPTION A.** [**RECOMMENDED**] Install from **PyPi**:

```sh
pip install -U potato-util
```

**OPTION B.** Install latest version directly from **GitHub** repository:

```sh
pip install git+https://github.com/bybatkhuu/module-python-utils.git
```

**OPTION C.** Install from the downloaded **source code**:

```sh
# Install directly from the source code:
pip install .

# Or install with editable mode:
pip install -e .
```

**OPTION D.** Install for **DEVELOPMENT** environment:

```sh
pip install -e .[dev]
```

**OPTION E.** Install from **pre-built release** files:

1. Download **`.whl`** or **`.tar.gz`** file from [**releases**](https://github.com/bybatkhuu/module-python-utils/releases)
2. Install with pip:

```sh
# Install from .whl file:
pip install ./potato_util-[VERSION]-py3-none-any.whl

# Or install from .tar.gz file:
pip install ./potato_util-[VERSION].tar.gz
```

**OPTION F.** Copy the **module** into the project directory (for **testing**):

```sh
# Install python dependencies:
pip install -r ./requirements.txt

# Copy the module source code into the project:
cp -r ./src/potato_util [PROJECT_DIR]
# For example:
cp -r ./src/potato_util /some/path/project/
```

## 🚸 Usage/Examples

### Simple

[**`examples/simple/main.py`**](./examples/simple/main.py):

```python
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
```

👍

---

### 🌎 Environment Variables

[**`.env.example`**](./.env.example):

```sh
# ENV=LOCAL
# DEBUG=false
# TZ=UTC
```

---

## 🧪 Running Tests

To run tests, run the following command:

```sh
# Install python test dependencies:
pip install .[test]

# Run tests:
python -m pytest -sv -o log_cli=true
# Or use the test script:
./scripts/test.sh -l -v -c
```

## 🏗️ Build Package

To build the python package, run the following command:

```sh
# Install python build dependencies:
pip install -r ./requirements/requirements.build.txt

# Build python package:
python -m build
# Or use the build script:
./scripts/build.sh
```

## 📝 Generate Docs

To build the documentation, run the following command:

```sh
# Install python documentation dependencies:
pip install -r ./requirements/requirements.docs.txt

# Serve documentation locally (for development):
mkdocs serve -a 0.0.0.0:8000
# Or use the docs script:
./scripts/docs.sh

# Or build documentation:
mkdocs build
# Or use the docs script:
./scripts/docs.sh -b
```

## 📚 Documentation

- [Docs](./docs)

---

## 📑 References

- <https://packaging.python.org/en/latest/tutorials/packaging-projects>
- <https://python-packaging.readthedocs.io/en/latest>
