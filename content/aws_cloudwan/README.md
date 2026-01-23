# AWS Cloud WAN Design Content

This directory contains all content for AWS Cloud WAN network design documentation.

## Versions

| Version | Status | Release Date | Notes |
|---------|--------|--------------|-------|
| v1.0.0  | Stable | 2026-01-16   | Initial release |

## Content Structure

Each version contains:

```
v{version}/
├── markdown/           # Documentation markdown files
├── templates/          # Terraform/CloudFormation templates
├── xlsx_templates/     # Excel input templates
└── images/            # Architecture diagrams and screenshots
```

## Markdown Files

| File | Label(s) | Description |
|------|----------|-------------|
| Overview.md | core_network | Introduction and prerequisites |
| CloudWANCoreNetworks.md | core_network | Core network configuration |
| CloudWANSegments.md | segments | Segment configuration |
| SegmentSharing.md | segment_sharing | Inter-segment connectivity |
| SegmentStaticRouting.md | static_routes | Static route configuration |
| ServiceInsertionAndNetworkFunctionGroup.md | network_function_groups | NFG setup |
| Monitoring.md | monitoring | CloudWatch integration |
| IngressDesign.md | ingress_design | Ingress architecture patterns |

## Labels

Labels are defined in `/config/labels/aws_cloudwan.yaml` and determine which markdown files are included in generated documents based on user selections.

## Adding New Content

1. Create/update markdown files in the appropriate version's `markdown/` directory
2. Update the label configuration if adding new features
3. Test document assembly with the new content
4. Update version and release notes
