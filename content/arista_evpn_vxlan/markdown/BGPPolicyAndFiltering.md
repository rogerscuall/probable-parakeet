# BGP Policy and Filtering

## Overview

Policy controls which routes are advertised, accepted, and preferred across the
fabric. In an EVPN VXLAN design, policy is applied both in the underlay (keep it
lean) and in the overlay (control tenant scope and route leaking).

## Underlay Policy

Keep the underlay table minimal and predictable:

- Advertise only loopbacks and point-to-point links.
- Reject anything else inbound with a tight prefix list.
- Preserve full ECMP — do not let policy collapse equal-cost paths.

## Overlay Policy (EVPN)

### Route Target Filtering

RTs decide which VRFs a route is imported into. Selective RT import/export is the
primary tool for stitching VRFs together and for limiting which VNIs cross a
border or DCI.

### Selective VNI Advertisement

Advertise only the VNIs a device actually needs. This reduces EVPN table size on
border and DCI nodes and contains the blast radius of misconfiguration.

### Route Leaking Between VRFs

Controlled inter-VRF connectivity (e.g. shared services) is achieved by importing
selected RTs across VRFs or via a service insertion point. Default behavior is
full isolation.

## Tools

| Tool | Use |
|------|-----|
| Prefix lists | Match underlay/overlay prefixes for permit/deny |
| Route maps | Combine matches with set actions (community, local-pref) |
| Communities / extended communities | Tag and classify routes (incl. RTs) |
| AS-path filters | Constrain eBGP propagation |

## Stability Features

- **Aggregation / summarization** — summarize Type-5 prefixes at borders.
- **Dampening / suppression** — limit churn from flapping routes.
- **Maximum-prefix** — protect control plane from runaway advertisement.

## Best Practices

- Define a consistent RT scheme before deployment and document it.
- Apply policy symmetrically (import and export) to avoid one-way reachability.
- Test policy changes against EVPN route counts, not just connectivity.

## Related

- [BGP Address Families](BGPAddressFamilies.md)
- [EVPN Route Types](EVPNRouteTypes.md)
