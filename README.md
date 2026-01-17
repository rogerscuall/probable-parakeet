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

| Design Type     | Description                                    |
|-----------------|------------------------------------------------|
| aws_cloudwan    | AWS Cloud WAN network architecture             |
| azure_vwan      | Azure Virtual WAN (future)                     |
| gcp_ncc         | Google Cloud Network Connectivity Center       |
| multi_cloud     | Multi-cloud networking patterns (future)       |

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

## Syncing Content

Content can be synced from remote storage:

```bash
# From S3
aws s3 sync s3://bucket/remote_location ./remote_location

# From Git
git clone --sparse https://github.com/org/repo.git
cd repo && git sparse-checkout set remote_location
```
