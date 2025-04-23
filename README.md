# Automatic Conformance Checking Insights in Celonis

![python version](https://img.shields.io/badge/python-3.12-blue)
![Mypy](https://img.shields.io/badge/mypy-checked-blue)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

This repository contains the code for the software lab "Automatic Conformance Checking Insights in Celonis", offered by the Chair for [Process and Data Science](https://www.pads.rwth-aachen.de/) at RWTH Aachen University.

## Installation

For installing the project's dependencies, we recommend using [uv](https://docs.astral.sh/uv/) as it operates very quickly.
To install the project's dependencies using uv, follow these steps:

  1. Ensure that you have uv installed on your system (see [here](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions).
  2. Clone the repository to your local machine.
  3. Navigate to the root directory of the repository.
  4. Run `uv sync`. uv will then install all necessary dependencies and create a virtual environment in the `.venv` folder at the root of the project.
  5. Activate the environment by running `source ./.venv/bin/activate` on Mac and Linux, or `.venv\Scripts\activate` on Windows.

Now you are ready to start.

### Developer Installation

As a developer, you should also initialize the pre-commit setup.
This enforces strict rules when committing to the repository, resulting in a very good code style.
There are different hooks that run, which enforce consistent styling and formatting of docstrings and code in general.

After installing the developer dependencies via `uv sync`, initialize the pre-commit hooks with the command `pre-commit install`.
After staging the files, when you commit them, all hooks run.
If a hook fails, for example, the ruff hook, because it had to reformat your file, you have to add that file again to the staging area (`git add <filename>`) and try committing again (`git commit`).

**Notice:** The virtual environment has to be activated in order to run all pre-commit hooks.

#### Code Style

We recommend this [Python styleguide](https://github.com/iai-group/guidelines/tree/main/python).
It mostly complies with the rules enforced by [Ruff](https://docs.astral.sh/ruff/) and with the hooks in the pre-commit setup.

#### Commit Style

We follow this [commit styleguide](https://github.com/iai-group/guidelines/blob/main/github/Git_commit.md).
It ensures that all commit messages follow the same format and are descriptive and readable.

## Contribution Workflow

We use a classic *feature-branch* workflow, where a new branch is created for every feature or bug fix.
Then a pull request is opened, which is then merged into the main branch of the project.
In addition to that, the main branch is protected, so there cannot be any commits to it directly, which enforces the above-described workflow.
