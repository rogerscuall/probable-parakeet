# Network Segments

## Overview

Segments provide logical isolation within your Cloud WAN. They allow you to group VPCs and other attachments based on business requirements, security policies, or traffic patterns.---

## Segment Design Considerations

### Naming Convention

Use consistent naming that reflects the segment's purpose:

- `production` - Production workloads
- `development` - Dev/test environments
- `shared-services` - Common infrastructure
- `dmz` - Internet-facing workloads

### Isolation Settings

**Isolate Attachments:**
- `true`: VPCs within the segment cannot communicate with each other
- `false`: VPCs within the segment can communicate

**Require Attachment Acceptance:**
- `true`: New VPC attachments require manual approval
- `false`: VPC attachments are automatically accepted

## Common Segment Patterns

### Hub-and-Spoke
```
shared-services (hub)
    ├── production (spoke)
    ├── development (spoke)
    └── dmz (spoke)
```

### Tiered Security
```
dmz (internet-facing)
    └── application (internal apps)
        └── database (data tier)
```

## Configuration Reference

| Field | Description | Required |
|-------|-------------|----------|
| name | Unique segment identifier | Yes |
| description | Human-readable description | No |
| edge_locations | AWS Regions for this segment | Yes |
| isolate_attachments | Isolate VPCs within segment | Yes |
| require_attachment_acceptance | Manual approval required | Yes |
