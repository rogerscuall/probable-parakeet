# Border Leaf Architecture

## Purpose

Border leaf switches connect the EVPN VXLAN fabric to everything outside it:
WAN, Internet, campus networks, or other data center sites. They are the Layer 3
gateway between the overlay and external routing domains and the point where
EVPN routes are exchanged with non-fabric networks.

## Key Functions

- Layer 3 gateway to external networks
- EVPN Type-5 route redistribution (fabric ↔ external)
- Data Center Interconnect (DCI) with stretched VLANs/VRFs
- Integration point for NAT and external firewall services

## Border Types

The `border_type` column records the external role of each border leaf.

| border_type | Role |
|-------------|------|
| internet_edge | Egress/ingress for Internet traffic |
| wan_edge | MPLS, SD-WAN, or leased-line connectivity |
| campus_edge | Integration with an existing campus LAN |
| dci_edge | EVPN multi-site over VXLAN or MPLS transport |

## Design Patterns

### Centralized Border

A dedicated border leaf pair handles all external connectivity. Clean separation
of concerns and a single policy enforcement point; all north-south traffic
hairpins through this pair.

### Distributed Border

Compute leaves also peer externally. Removes the hairpin for locally sourced
external traffic but spreads policy across many devices.

### Hierarchical (Border + Firewall)

Border ↔ firewall ↔ fabric, so all external traffic is inspected before entering
the overlay. Commonly paired with [Service Insertion](ServiceInsertionOverview.md).

## External Routing

Border leaves typically run eBGP toward external peers using `external_asn`.
Fabric prefixes (EVPN Type-5) are redistributed outward, and external/default
routes are injected back into the relevant VRFs.

## Configuration Reference

Border data is entered in the **BorderLeaf** sheet.

| Field | Description | Required |
|-------|-------------|----------|
| hostname | Unique device identifier | Yes |
| border_type | One of the border types above | Yes |
| external_asn | BGP ASN of the external peer | No |

## Related

- [Data Center Interconnect](DataCenterInterconnect.md)
- [EVPN Route Types](EVPNRouteTypes.md)
