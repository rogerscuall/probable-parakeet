# Firewall Integration

## Overview

Firewalls are the most common service inserted into an EVPN VXLAN fabric. They
enforce policy between tenants (VRFs), between security zones, and at the
fabric's external edge. This document covers the common patterns for attaching
firewalls and steering traffic through them.

## Insertion Patterns

### Inter-VRF Firewall (Routed)

The firewall sits between two VRFs and is the only path connecting them. Because
inter-VRF traffic is blocked by default, all tenant-to-tenant flows are forced
through the firewall.

```
 VRF-A  ---->  [ Firewall ]  ---->  VRF-B
        (routed insertion, stateful inspection)
```

### Transparent (L2) Firewall

The firewall bridges two VLANs of the same subnet via VLAN stitching. Hosts keep
their gateway; the firewall inspects traffic transparently at Layer 2.

### Perimeter Firewall (Border)

The firewall is positioned at the border leaf so all north-south traffic is
inspected before entering or leaving the fabric. See
[Border Leaf Architecture](BorderLeafArchitecture.md).

## Ensuring Flow Symmetry

Firewalls are stateful, so both directions of a flow must traverse the same
firewall node. Achieve this by:

- Avoiding ECMP across non-synchronized firewall nodes.
- Using active/standby pairs, or active/active clusters with flow-state sync.
- Designing return routing to match the forward path.

## High Availability

- Deploy redundant firewalls and synchronize session state.
- Use the same VRF/`insertion_mode` on both members.
- Validate failover does not break established sessions.

## Configuration Reference

Record the firewall in the **ServiceInsertion** sheet with
`service_type: firewall` and the appropriate `insertion_mode` (`routed` or
`transparent`) and `vrf`.

## Related

- [Service Insertion Overview](ServiceInsertionOverview.md)
- [Load Balancer Integration](LoadBalancerIntegration.md)
