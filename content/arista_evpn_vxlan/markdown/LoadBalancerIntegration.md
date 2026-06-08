# Load Balancer Integration

## Overview

Load balancers (ADCs) distribute traffic across pools of servers and often
terminate SSL/TLS. Integrating them into an EVPN VXLAN fabric requires deciding
where the VIPs live, how return traffic flows, and how the appliance attaches to
the overlay.

## Deployment Modes

### Two-Arm (Routed)

The load balancer has separate client-side and server-side interfaces in
different subnets/VRFs. It routes between them and is a natural policy point.

### One-Arm

The load balancer connects on a single interface. Traffic is policy-routed to the
VIP and returned via Source-NAT so the server replies traverse the LB. Maps to
`insertion_mode: one_arm`.

```
 client --> VIP on LB (one-arm) --SNAT--> server pool
                  ^------------- return ----------/
```

### Direct Server Return (DSR)

The server replies directly to the client, bypassing the LB on the return path.
High throughput but requires careful overlay and ARP handling; flow symmetry
no longer holds, so avoid placing stateful firewalls in the same path.

## VIP Placement

- Advertise VIPs into EVPN as host routes (Type-5 /32) so they are reachable
  fabric-wide and can move between LB nodes.
- Keep the VIP subnet in the appropriate tenant VRF.

## High Availability

- Active/active or active/standby LB clusters with health monitoring.
- Ensure VIP failover re-advertises reachability promptly via EVPN.

## Configuration Reference

Record the load balancer in the **ServiceInsertion** sheet with
`service_type: load_balancer`, the chosen `insertion_mode`, and the `vrf` that
hosts the VIPs.

## Related

- [Service Insertion Overview](ServiceInsertionOverview.md)
- [Firewall Integration](FirewallIntegration.md)
