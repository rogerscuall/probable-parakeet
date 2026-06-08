# Super Spine Design Patterns

## Topology Patterns

### Single Plane

All pod spines connect to a single set of Super Spine nodes. Simplest to operate
and adequate for most multi-pod fabrics.

### Multi-Plane

Super Spine nodes are organized into independent planes. Each pod spine connects
to one node per plane. Planes provide fault isolation and incremental bandwidth
scaling — losing a plane degrades capacity but never disconnects a pod.

```
Plane A:  SS-A1   SS-A2
Plane B:  SS-B1   SS-B2
            \  \  /  /
             pod spines
```

## ASN Allocation

In an eBGP underlay every device uses a unique private ASN so that BGP path
selection and loop prevention work naturally across the Clos.

| Tier | ASN strategy |
|------|--------------|
| Super Spine | Single shared ASN, or unique per node |
| Spine | Unique ASN per pod (shared by the pod's spines) |
| Leaf | Unique ASN per leaf (or per MLAG pair) |

Using a single ASN on all Super Spines lets pod spines treat them as one logical
upstream and keeps `allowas-in` rules predictable.

## Underlay Routing

- **eBGP** is the recommended underlay protocol: explicit ASNs, simple policy,
  and deterministic ECMP. This template assumes eBGP.
- Advertise only loopbacks and point-to-point links into the underlay.
- Enable **BFD** on Super Spine ↔ Spine links for sub-second failure detection.
- Maintain full ECMP fan-out — every pod spine should reach every Super Spine.

## Overlay Boundary

The Super Spine stays out of the EVPN overlay. Overlay BGP (EVPN address family)
peers between leaf VTEPs and the pod spines acting as route reflectors. The Super
Spine only needs to carry VTEP loopback reachability in the underlay so that VXLAN
tunnels between pods can form.

## Scaling and Availability

- Add Super Spine nodes (or planes) to grow inter-pod bandwidth linearly.
- Keep oversubscription between Spine→Super Spine consistent across pods.
- Deploy at least two nodes per plane; size so that N-1 still meets SLA.
