# Service Insertion & Network Function Groups

## Overview

Network Function Groups (NFGs) enable service insertion, allowing you to route traffic through network appliances such as firewalls, IDS/IPS systems, or load balancers.

## Architecture

```
┌─────────┐    ┌─────────────────┐    ┌─────────┐
│ Source  │ -> │ Network Function│ -> │  Dest   │
│ Segment │    │ Group (Firewall)│    │ Segment │
└─────────┘    └─────────────────┘    └─────────┘
```

## Network Function Group Configuration

| Field | Description | Required |
|-------|-------------|----------|
| name | Unique NFG identifier | Yes |
| description | Human-readable description | No |
| require_attachment_acceptance | Manual approval for appliances | Yes |

## Traffic Routing Options

### Send Via
Routes traffic between two segments through an NFG for inspection:
- Source segment → NFG → Destination segment
- Commonly used for east-west traffic inspection

### Send To
Routes traffic from a segment directly to an NFG as the destination:
- Source segment → NFG (terminal)
- Used for NAT gateways, proxies, or centralized services

## Use Cases

1. **Centralized Firewall Inspection**
   - All inter-segment traffic flows through firewall NFG

2. **Egress Filtering**
   - Internet-bound traffic routes through proxy NFG

3. **Load Balancing**
   - Application traffic distributes across multiple targets

## Best Practices

- Use high-availability appliance deployments
- Monitor NFG performance and capacity
- Implement health checks for appliances
- Document traffic flow patterns
