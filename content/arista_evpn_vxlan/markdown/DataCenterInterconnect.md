# Data Center Interconnect (DCI)

## Overview

Data Center Interconnect extends fabric connectivity between physically separate
sites. In an EVPN VXLAN design, DCI carries selected VRFs and/or VLANs between
data centers so that tenants and workloads span locations while preserving
segmentation and policy.

## EVPN Multi-Site

The recommended approach is **EVPN Multi-Site**, where each site is an
independent fabric and border (gateway) nodes interconnect them. Benefits:

- **Fault containment** — failures and BUM scope are isolated per site.
- **Control-plane summarization** — sites exchange only the routes they need.
- **Independent operations** — each site can be upgraded or maintained alone.

```
   Site A fabric            Site B fabric
   [ border/DCI ] === transport === [ border/DCI ]
        VXLAN or MPLS between sites
```

## Transport Options

| Transport | Notes |
|-----------|-------|
| VXLAN over IP | Reuses the EVPN data plane end-to-end; simplest when an IP WAN exists |
| MPLS / L3VPN | Integrates with existing service-provider or core MPLS |
| Dark fiber / DWDM | Direct site-to-site links for high bandwidth, low latency |

## What to Stretch

- **Layer 3 (preferred)**: extend VRFs and route between sites with EVPN Type-5.
  Keeps Layer 2 fault domains local.
- **Layer 2 (when required)**: stretch specific VLANs/VNIs for clustering or live
  migration. Limit the scope and rely on EVPN to suppress unnecessary flooding.

## Design Considerations

- Use border leaves with `border_type: dci_edge` as the interconnect gateways.
- Apply consistent RD/RT policy so stretched VRFs import correctly across sites.
- Filter which VNIs are advertised across the DCI to control blast radius.
- Plan for asymmetric bandwidth and latency on the inter-site path.

## Related

- [Border Leaf Architecture](BorderLeafArchitecture.md)
- [EVPN Route Types](EVPNRouteTypes.md)
