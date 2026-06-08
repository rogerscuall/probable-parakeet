# Leaf Layer Overview

## Introduction

Leaf switches provide connectivity to compute, storage, and services, and act as
**VXLAN Tunnel Endpoints (VTEPs)** for the overlay. They originate and terminate
VXLAN encapsulation and advertise host reachability into EVPN.

## Responsibilities

- VTEP for VXLAN encapsulation / decapsulation
- Anycast gateway for first-hop routing of attached hosts
- EVPN Type-2 (MAC/IP) and Type-5 (IP prefix) route advertisement
- MLAG peering for dual-homed host redundancy

## Common Leaf Types

| Type | Purpose |
|------|---------|
| compute | Server connectivity (ESXi, bare metal, hypervisors) |
| storage | SAN/NAS connectivity, often with specialized QoS |
| service | Firewalls, load balancers, and other appliances |
| border | External / DCI connectivity (see Border Leaf) |

The `leaf_type` column lets you record the intended role of each leaf so the
generated design and downstream automation can apply the right profile.

## Redundancy with MLAG

Leaves are typically deployed in pairs forming an **MLAG domain** so that hosts
can be dual-homed with an active/active LAG. Within EVPN, the pair shares a
common VTEP (anycast VTEP) loopback so either switch can forward overlay traffic.

- `mlag_domain_id` groups the two switches of a pair.
- Both members advertise the same shared VTEP loopback for the pair.

## Configuration Reference

Data for this layer is entered in the **Leaf** sheet of the template.

| Field | Description | Required |
|-------|-------------|----------|
| hostname | Unique device identifier | Yes |
| asn | BGP autonomous system number | Yes |
| vtep_loopback | VXLAN source loopback (shared within an MLAG pair) | Yes |
| mlag_domain_id | Identifier grouping an MLAG pair | No |
| leaf_type | `compute`, `storage`, `service`, or `border` | Yes |

## Related

- [VXLAN and VTEP](VXLANandVTEP.md)
- [Anycast Gateway](AnycastGateway.md)
- [Border Leaf Architecture](BorderLeafArchitecture.md)
