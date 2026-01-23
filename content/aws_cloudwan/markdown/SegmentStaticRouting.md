# Static Routing

## Overview

Static routes allow you to define explicit routing paths within your Cloud WAN segments. This is useful for routing traffic to specific destinations that aren't automatically propagated.

## Route Types

### Static Routes
Direct traffic to a specific destination through a defined next hop.

### Blackhole Routes
Drop traffic destined for specific prefixes. Useful for:
- Blocking known malicious IP ranges
- Preventing routing loops
- Implementing security policies

## Configuration Fields

| Field | Description | Required |
|-------|-------------|----------|
| segment | Target segment for the route | Yes |
| route_type | `static` or `blackhole` | Yes |
| prefix | Destination CIDR block | Yes |
| next_hop | Attachment ID (for static routes) | For static |
| region | Region for regional routes | Yes |
| comments | Documentation | No |

## Common Use Cases

1. **On-premises connectivity**: Route traffic to Transit Gateway attachments
2. **Internet egress**: Direct traffic to NAT gateways or firewalls
3. **Service access**: Route to PrivateLink endpoints
4. **Security filtering**: Blackhole malicious prefixes

## Best Practices

- Document all static routes with clear comments
- Use the most specific prefix possible
- Regularly audit and clean up unused routes
- Test route changes in non-production first
