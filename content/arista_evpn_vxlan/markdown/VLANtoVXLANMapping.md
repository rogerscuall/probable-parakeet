# VLAN to VXLAN Mapping

## Overview

VLANs provide Layer 2 segmentation locally on a leaf, while VXLAN extends those
segments across the Layer 3 fabric. Each VLAN is mapped to a Layer 2 **VNI** so
that hosts in the same segment communicate regardless of which leaf they attach
to.

## Local VLAN vs. Global VNI

- A **VLAN ID** is locally significant to a switch (and limited to 1–4094).
- A **VNI** is globally significant across the fabric (24-bit, ~16M values).
- The leaf maps `vlan_id` → `vni`. Two leaves can even use different local VLAN
  IDs for the same VNI, though keeping them consistent is strongly recommended
  for operational clarity.

```
 leaf1: VLAN 10  ->  VNI 10010  <---- same VNI ----> VNI 10010  <- VLAN 10 :leaf2
                         (one stretched L2 segment)
```

## Mapping Strategy

A common convention encodes the VLAN in the VNI for readability, e.g. VLAN 10 →
VNI 10010, VLAN 20 → VNI 10020. The L2 VNI (per-VLAN) is distinct from the L3 VNI
(per-VRF) used for routing — see [VRFs and Tenant Isolation](VRFsAndTenantIsolation.md).

## Anycast Gateway Association

Each routed VLAN also carries an anycast gateway so hosts have a local first hop.
The `anycast_gateway` and `vrf` columns tie the segment to its Layer 3 context.
See [Anycast Gateway](AnycastGateway.md).

## Configuration Reference

VLAN data is entered in the **VLANs** sheet.

| Field | Description | Required |
|-------|-------------|----------|
| vlan_id | Local VLAN ID (1–4094) | Yes |
| vni | L2 VNI the VLAN maps to | Yes |
| anycast_gateway | Distributed gateway IP/mask for the subnet | Yes |
| vrf | Parent VRF for the subnet | Yes |

## Best Practices

- Keep VLAN↔VNI mapping consistent fabric-wide.
- Reserve distinct ranges for L2 VNIs and L3 VNIs to avoid confusion.
- Document which VRF each VLAN belongs to before deployment.
