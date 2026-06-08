# VRFs and Tenant Isolation

## Overview

VRFs (Virtual Routing and Forwarding instances) provide Layer 3 isolation in the
overlay. Each VRF is an independent routing table, carried across the fabric by a
Layer 3 VNI and EVPN Type-5 (IP-prefix) routes. VRFs are the primary tool for
multi-tenancy and security segmentation.

## VRF Components

| Element | Purpose |
|---------|---------|
| VRF name | Logical tenant / routing domain identifier |
| L3 VNI | VXLAN identifier used for inter-subnet routing within the VRF |
| Route Distinguisher (RD) | Makes overlapping tenant prefixes globally unique in BGP |
| Route Target (RT) | Controls import/export of routes between VTEPs |

## Route Distinguisher and Route Target

- The **RD** is prepended to each prefix so two tenants can use the same IP space
  without colliding in the EVPN table. A common convention is
  `<router-id>:<vni>` or `<asn>:<vni>`.
- The **RT** governs which VRFs a route is imported into. Matching export and
  import RTs on a set of VTEPs stitches a VRF together across the fabric.

## Common Use Cases

- **Tenant separation** in multi-tenant / shared infrastructure
- **Environment isolation** — production / staging / development
- **Security zones** — trusted / DMZ / untrusted
- **Application tiers** — web / app / database

Inter-VRF communication is deliberately blocked by default; route leaking or a
service insertion point (firewall) is required to connect tenants.

## Configuration Reference

VRF data is entered in the **VRFs** sheet.

| Field | Description | Required |
|-------|-------------|----------|
| vrf_name | Unique VRF / tenant name | Yes |
| vni | L3 VNI associated with the VRF | Yes |
| route_distinguisher | RD value, e.g. `65001:50001` | Yes |

VLANs reference their parent VRF via the `vrf` column in the VLANs sheet.

## Related

- [VLAN to VXLAN Mapping](VLANtoVXLANMapping.md)
- [EVPN Route Types](EVPNRouteTypes.md)
