# Anycast Gateway

## The Problem It Solves

In a fabric where workloads move between racks, the default gateway for a subnet
must be reachable from any leaf. A traditional centralized gateway forces traffic
to hairpin to one switch. The **distributed anycast gateway** places the same
gateway IP and MAC on every leaf that hosts the subnet, so the first hop is always
local.

## How It Works

- Every leaf serving a VLAN configures the **same SVI IP** (the `anycast_gateway`)
  and the **same virtual MAC** for that subnet.
- A host's traffic is routed by whichever leaf it is attached to — no hairpin.
- After a VM migrates to another rack, its gateway is still directly attached, so
  there is no re-ARP or sub-optimal path.

```
 host A (rack 1)            host B (rack 2)
     |                          |
  leaf1  SVI 10.1.1.1/24    leaf2  SVI 10.1.1.1/24   <-- identical anycast GW
     \________ VXLAN overlay (same VNI) _________/
```

## Symmetric IRB

This design uses **symmetric Integrated Routing and Bridging (IRB)**: routing
between subnets happens through a per-VRF Layer 3 VNI, and both the ingress and
egress VTEP perform a routing step. Symmetric IRB scales better than asymmetric
because each VTEP only needs the VNIs and routes for locally attached subnets.

## Configuration Reference

Anycast gateway values are entered in the **VLANs** sheet.

| Field | Description | Required |
|-------|-------------|----------|
| vlan_id | Local VLAN mapped to the VNI | Yes |
| vni | VXLAN identifier for the L2 segment | Yes |
| anycast_gateway | Gateway IP with mask, e.g. `10.1.1.1/24` | Yes |
| vrf | VRF the subnet belongs to | Yes |

Use a consistent anycast gateway IP and mask for a given subnet across every leaf
that serves it. The virtual MAC is applied fabric-wide and is typically a single
shared value.

## Related

- [VLAN to VXLAN Mapping](VLANtoVXLANMapping.md)
- [VRFs and Tenant Isolation](VRFsAndTenantIsolation.md)
