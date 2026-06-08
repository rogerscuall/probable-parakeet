# EVPN Route Types

## Overview

EVPN uses BGP NLRI "route types" to advertise different kinds of reachability.
Understanding them is key to troubleshooting and to deciding between bridging and
routing in the overlay.

## The Route Types in This Design

| Type | Name | Carries |
|------|------|---------|
| Type-2 | MAC/IP Advertisement | Host MAC, and optionally MAC+IP for ARP suppression and host routing |
| Type-3 | Inclusive Multicast Ethernet Tag | VTEP membership per VNI; builds the BUM flood list |
| Type-4 | Ethernet Segment | ES discovery for multihoming / designated forwarder election |
| Type-5 | IP Prefix | Routed prefixes (subnets, summaries, /32 host routes) per VRF |

## Type-2 — MAC/IP

The workhorse of the overlay. Advertises where each MAC lives, enabling unicast
VXLAN forwarding without flooding. When it includes the IP, it also enables:

- **ARP/ND suppression** — leaves answer ARP locally from EVPN state.
- **Host mobility** — a sequence number tracks moves so the latest location wins.

## Type-3 — Inclusive Multicast

Each VTEP advertises its membership in a VNI so other VTEPs know where to send
BUM traffic. With ingress replication this builds the per-VNI replication list.
See [BUM Traffic Optimization](BUMTrafficOptimization.md).

## Type-5 — IP Prefix

Used for **symmetric IRB** routing and for advertising subnets, summaries, and
external/host routes between VRFs and across the DCI. Type-5 decouples routing
from MAC learning, which is what makes large-scale and inter-site routing
efficient.

## Type-4 — Ethernet Segment

Supports EVPN multihoming: VTEPs sharing an Ethernet Segment (e.g. an MLAG pair
or ESI-LAG) elect a designated forwarder and apply split-horizon so a dual-homed
host never receives duplicate BUM frames.

## Practical Notes

- Type-2 and Type-5 together cover almost all data-plane needs.
- Watch sequence numbers on Type-2 routes when diagnosing host-move issues.
- Filter Type-5 advertisement across the DCI to control route scale.

## Related

- [BGP Address Families](BGPAddressFamilies.md)
- [VRFs and Tenant Isolation](VRFsAndTenantIsolation.md)
