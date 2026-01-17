# Segment Sharing

## Overview

Segment Sharing enables controlled communication between different network segments. By default, segments are completely isolated from each other.

## Configuration

Sharing is configured as segment pairs. When sharing is enabled between two segments, resources in each segment can communicate with resources in the other segment.

### Example Configuration

| Segment A | Segment B | Sharing Enabled | Use Case |
|-----------|-----------|-----------------|----------|
| production | shared-services | Yes | Production access to shared infrastructure |
| development | shared-services | Yes | Dev access to shared tools |
| production | development | No | Keep production isolated from dev |

## Best Practices

1. **Principle of Least Privilege**: Only enable sharing where necessary
2. **Document Justification**: Record why each sharing relationship exists
3. **Regular Review**: Periodically audit sharing configurations
4. **Security Controls**: Use security groups and NACLs for additional control

## Implementation Notes

- Sharing is bidirectional by default
- For unidirectional traffic, use route table controls
- Consider using Network Function Groups for inspection between segments
