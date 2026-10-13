# Local builds with uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then copy
the published pipeline resources into the generated project root alongside
`inventory.yml`, `group_vars/`, and optional `host_vars/`:

```sh
make install
make validate
make build
# Equivalent build alias:
make build-all
# Custom inventory and fabric:
make build INVENTORY=avd/inventory.yml FABRIC=DC1_FABRIC
```

No virtual environment activation or system Python package installation is
needed. `make install` initializes a bare uv project if `pyproject.toml` is
absent, imports the pinned dependencies from `requirements.txt` with `uv add`,
and creates `.venv` and `uv.lock`. It then installs the collections from
`requirements.yml` into `.ansible/collections` using `uv run ansible-galaxy`.
Repeated installation preserves an existing project file and does not reinitialize
it. `make init` can also be run separately.

The project and lockfile are generated locally because the published manifest
does not include them. Keep the generated `uv.lock` in a consuming project's
version control if it needs reproducible transitive dependency versions. The
bundle continues to use `requirements.txt` as its Python dependency source;
keep the PyAVD and collection pins aligned at 5.7.3.

Every validation and build command runs through `uv run`, including the Python
validator and its `ansible-inventory` subprocess. Make sets `ANSIBLE_CONFIG`
and `ANSIBLE_COLLECTIONS_PATH` to this project's paths. Build outputs remain in
`intended/` and `documentation/`, including with a nested inventory.

The default interpreter is Python 3.12; uv can download it if needed. Override
it with `PYTHON=3.12` or an interpreter path, and override the uv executable
with `UV=/path/to/uv`. Install before validating or building. Changing the Python
version should be followed by `make install`.

The existing `.gitlab-ci.yml` is unchanged. This repository has no GitHub Actions
workflow; the verification below exercises both jobs from its GitLab definition
using uv locally. Python dependency installation uses `uv pip install` (uv has
no `install` subcommand), and collection installation, schema validation, syntax
validation, and configuration generation use `uv run`.

## Verification and evidence

From this directory, run:

```sh
python3 tests/verify_uv.py
```

This test requires uv, make, network access to Python/PyPI/Ansible Galaxy, and
a Python 3 interpreter for the test driver. It creates a fresh consumer under
`tests/.work/` using only resources already listed in `pipeline/manifest.json`.
The four-switch fixture has two spines and two independent L3 leaves with eBGP
underlay and EVPN/VXLAN overlay. It does not connect to network devices.

The test checks initialization, actual virtual environment creation, dependency
and collection installation, repeat installation, every Make target, both CI
jobs with uv, inventory/fabric overrides, and rejection of missing inventory,
missing fabric, and invalid AVD inputs. It checks generated hostnames, VXLAN
interfaces, and device documentation. Full command output and exit codes are
in `tests/evidence/verification.log`; `tests/evidence/results.json` contains
check results and generated artifact sizes and SHA-256 hashes. Temporary
projects, Python downloads, caches, collections, and build outputs stay under
`tests/.work/`, which is ignored by Git. Rerunning replaces that scratch directory
and the evidence files.
