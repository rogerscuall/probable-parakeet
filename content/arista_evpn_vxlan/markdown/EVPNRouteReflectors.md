# EVPN Route Reflectors

## Why Route Reflection

In an EVPN VXLAN fabric the leaf VTEPs must exchange overlay reachability
(MAC, MAC/IP, and IP-prefix routes). A full mesh of iBGP sessions between every
leaf does not scale, so the spines act as **route reflectors (RRs)**: each leaf
peers only with the spines, and the spines reflect EVPN routes to all other leaves.

```
   leaf1            leaf2            leaf3
     \  \           /  \           /  /
      \  \---------/    \---------/  /
       \      spine (RR)  spine (RR)
        EVPN sessions: leaf <-> spine only
```

## Control Plane Models

### iBGP with Route Reflectors

All devices share one ASN in the overlay. Spines are RRs; leaves are RR clients.
Standard, well-understood, and the assumption behind the `route_reflector` role
in the Spine sheet.

### eBGP Overlay (Route Server style)

When the underlay uses unique eBGP ASNs, the EVPN overlay can run over the same
eBGP sessions with the spines re-advertising routes. This avoids a separate iBGP
mesh but requires `next-hop-unchanged` so the originating VTEP remains the tunnel
endpoint.

## Key Configuration Requirements

- **Next-hop handling**: the VTEP loopback of the originating leaf must be
  preserved as the EVPN next hop so VXLAN tunnels point at the real endpoint.
- **Redundancy**: deploy two or more RRs; clients peer with all of them.
- **Cluster-id**: when multiple RRs are used, a consistent cluster-id prevents
  unnecessary route duplication.
- **RR placement**: spines are the natural RR location because every leaf
  already peers with every spine.

## Operational Guidance

- Keep RR configuration identical across spines for predictable behavior.
- Monitor EVPN session state and received/advertised route counts per leaf.
- An RR carries control-plane state only — it does not need to be a VTEP.

## Related

- [Spine Layer Overview](SpineLayerOverview.md)
- [EVPN Route Types](EVPNRouteTypes.md)
- [BGP Address Families](BGPAddressFamilies.md)
