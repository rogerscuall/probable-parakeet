# Spine Layer Overview

## Introduction

The Spine layer is the routing and switching backbone within a data center pod.
Every leaf connects to every spine, and all east-west traffic between leaves
transits the spine tier. In an EVPN VXLAN fabric the spines also serve as the
**BGP route reflectors** for the EVPN control plane.

## Design Principles

- **Pure Layer 3 operation** — spines route between leaves; no VLAN is stretched
  across spines. All Layer 2 adjacency lives in the VXLAN overlay.
- **Symmetric bandwidth** — every leaf has equal uplink capacity to every spine,
  giving predictable any-to-any throughput.
- **ECMP everywhere** — leaf uplinks are load-balanced across all spines.
- **Redundant control plane** — at least two spines so route reflection survives
  the loss of any single device.

## Underlay vs. Overlay Roles

| Plane | Spine role |
|-------|-----------|
| Underlay | eBGP (or OSPF) peer carrying loopback + P2P reachability |
| Overlay | iBGP EVPN route reflector (or eBGP RS) for leaf VTEPs |

A common deployment uses eBGP in the underlay and reflects EVPN routes by having
the spines act as route servers. See [EVPN Route Reflectors](EVPNRouteReflectors.md)
for the control-plane detail.

## Hardware Considerations

- Spine-class platforms (e.g., 7500R / 7280R) sized for leaf fan-out
- Line-rate L3 forwarding and sufficient route scale for the EVPN table
- Buffering appropriate to the workload's incast profile

## Configuration Reference

Data for this layer is entered in the **Spine** sheet of the template.

| Field | Description | Required |
|-------|-------------|----------|
| hostname | Unique device identifier | Yes |
| asn | BGP autonomous system number | Yes |
| loopback_ip | Router/RR loopback address | Yes |
| role | `route_reflector` or `spine` | Yes |

Set `role` to `route_reflector` for spines that reflect EVPN routes to the leaf
VTEPs, and `spine` for nodes that only provide underlay transport.
