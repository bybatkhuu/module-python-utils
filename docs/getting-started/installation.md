---
title: Installation
---

# 🛠 Installation

## 1. 📥 Download or clone the repository

[TIP] Skip this step, if you're going to install the package directly from **PyPi** or **GitHub** repository.

**1.1.** Prepare projects directory (if not exists):

```sh
# Create projects directory:
mkdir -pv ~/workspaces/projects

# Enter into projects directory:
cd ~/workspaces/projects
```

**1.2.** Follow one of the below options **[A]**, **[B]** or **[C]**:

**OPTION A.** Clone the repository:

```sh
git clone https://github.com/bybatkhuu/module.python-utils.git && \
    cd module.python-utils
```

**OPTION B.** Clone the repository (for **DEVELOPMENT**: git + ssh key):

```sh
git clone git@github.com:bybatkhuu/module.python-utils.git && \
    cd module.python-utils
```

**OPTION C.** Download source code:

1. Download archived **zip** file from [**releases**](https://github.com/bybatkhuu/module.python-utils/releases).
2. Extract it into the projects directory.

### 2. 📦 Install the package

[NOTE] Choose one of the following methods to install the package **[A ~ F]**:

**OPTION A.** [**RECOMMENDED**] Install from **PyPi**:

```sh
# Install from staging TestPyPi:
pip install -i https://test.pypi.org/simple -U potato_utils

# Or install from production PyPi:
# pip install -U potato_utils
```

**OPTION B.** Install latest version directly from **GitHub** repository:

```sh
pip install git+https://github.com/bybatkhuu/module.python-utils.git
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
pip install -r ./requirements/requirements.dev.txt
```

**OPTION E.** Install from **pre-built release** files:

1. Download **`.whl`** or **`.tar.gz`** file from [**releases**](https://github.com/bybatkhuu/module.python-utils/releases)
2. Install with pip:

```sh
# Install from .whl file:
pip install ./potato_utils-[VERSION]-py3-none-any.whl

# Or install from .tar.gz file:
pip install ./potato_utils-[VERSION].tar.gz
```

**OPTION F.** Copy the **module** into the project directory (for **testing**):

```sh
# Install python dependencies:
pip install -r ./requirements.txt

# Copy the module source code into the project:
cp -r ./src/potato_utils [PROJECT_DIR]
# For example:
cp -r ./src/potato_utils /some/path/project/
```
