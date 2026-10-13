# Remote Content Location

This directory serves as the centralized content repository for the Network Design Platform. It is designed to be hosted remotely (e.g., S3, Git repository, or CDN) and synced with the application.

## Directory Structure

```
remote_location/
├── README.md                          # This file
├── manifest.json                      # Version manifest for all content
├── config/
│   └── labels/                        # Design type label configurations
│       └── {design_type}.yaml         # Label definitions per design type
├── content/
│   └── design_types/                  # Content organized by design type
│       └── {design_type}/             # e.g., aws_cloudwan, azure_vwan
│           └── {version}/             # e.g., v1.0.0, v1.1.0
│               ├── markdown/          # Documentation markdown files
│               ├── templates/         # Code/config templates
│               ├── xlsx_templates/    # Excel template files
│               └── images/            # Design type specific images
└── shared/                            # Resources shared across design types
    ├── images/                        # Common images (logos, icons)
    ├── markdown/                      # Common documentation
    ├── templates/                     # Common templates
    └── schemas/                       # JSON schemas for validation
```

## Design Types

Each design type represents a specific network architecture:

| Design Type       | Description                                    |
|-------------------|------------------------------------------------|
| aws_cloudwan      | AWS Cloud WAN network architecture             |
| arista_evpn_vxlan | Arista EVPN VXLAN data center fabric           |
| azure_vwan        | Azure Virtual WAN (future)                     |
| gcp_ncc           | Google Cloud Network Connectivity Center       |
| multi_cloud       | Multi-cloud networking patterns (future)       |

## Versioning

Content is versioned using semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to label structure or content format
- **MINOR**: New labels, features, or significant content additions
- **PATCH**: Bug fixes, typo corrections, minor content updates

## Content Files

### Markdown Files
- Located in `content/design_types/{type}/{version}/markdown/`
- Referenced in label configuration via `content.markdown_files`
- Used by `DocumentAssembler` to build design documents

### XLSX Templates
- Located in `content/design_types/{type}/{version}/xlsx_templates/`
- Base templates for user input
- Contains sheet structure matching label `xlsx_sheets` references

### Images
- Design-specific images in `content/design_types/{type}/{version}/images/`
- Shared images in `shared/images/`

## Integration with Application

The application loads content from this location via filesystem or remote URL:

```go
// Example: Loading content from remote location
contentFS := os.DirFS("remote_location/content/design_types")
documentAssembler := services.NewDocumentAssembler(contentFS)
```

## Adding New Design Types

1. Create directory: `content/design_types/{new_type}/v1.0.0/`
2. Add subdirectories: `markdown/`, `templates/`, `xlsx_templates/`, `images/`
3. Create label config: `config/labels/{new_type}.yaml`
4. Update `manifest.json` with new design type

## Pipeline Resources

Pipeline bundles are published independently of design content. Consumers use
`https://raw.githubusercontent.com/rogerscuall/probable-parakeet/main/pipeline`
as the resource base URL and read `pipeline/manifest.json` to discover each
design type's files. Each `_files` array lists files relative to its containing
directory, including dotfiles; nested objects describe subdirectories.

The `arista_evpn_vxlan` bundle contains `.gitlab-ci.yml`, `Makefile`,
`ansible.cfg`, `build.yml`, `requirements.txt`, `requirements.yml`, and
`scripts/validate_avd.py`. For example, append
`/arista_evpn_vxlan/.gitlab-ci.yml` to the base URL to retrieve its CI definition.

Copy the contents of `pipeline/arista_evpn_vxlan/` into the generated project's
root, preserving the `scripts/` directory. The project supplies `inventory.yml`
and adjacent `group_vars/` and optional `host_vars/` directories; these are
design inputs, not resources supplied by this repository. The inventory must
contain the fabric group (default `FABRIC`) with switch hosts in it or its
descendant groups.

With Python 3.12 and a virtual environment activated, run:

```bash
make install
make build
# Override inventory location and fabric group if needed:
make build INVENTORY=avd/inventory.yml FABRIC=DC1_FABRIC
```

`make validate` resolves inventory variables using Ansible, validates fabric
hosts with the PyAVD schema, and checks playbook syntax. `make build` also runs
`eos_designs` and `eos_cli_config_gen`, which enforce AVD validation while
generating `intended/` configurations and `documentation/`. The GitLab pipeline
runs the same validation and build stages and retains both output directories
as artifacts. Set its `INVENTORY` and `FABRIC` CI variables for custom inputs.

Python dependencies and the Arista collection are pinned to the same AVD
version; update both requirement files together. Installation follows the
[AVD collection installation guide](https://avd.arista.com/5.7/docs/installation/collection-installation.html).
The playbook uses the build roles from the
[AVD single data center example](https://avd.arista.com/5.7/ansible_collections/arista/avd/examples/single-dc-l3ls/index.html).

## Syncing Content

Content can be synced from remote storage:

```bash
# From S3
aws s3 sync s3://bucket/remote_location ./remote_location

# From Git
git clone --sparse https://github.com/org/repo.git
cd repo && git sparse-checkout set remote_location
```
