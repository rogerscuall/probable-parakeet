# VXLAN and VTEP

## What VXLAN Provides

VXLAN (Virtual Extensible LAN) tunnels Layer 2 frames inside UDP/IP packets,
letting Layer 2 segments span an arbitrary Layer 3 underlay. Each segment is
identified by a 24-bit **VNI (VXLAN Network Identifier)**, allowing up to ~16M
segments versus the 4094 limit of traditional VLANs.

```
[ Original L2 frame ] --> [ VXLAN header (VNI) ] --> [ UDP ] --> [ IP/underlay ]
                          encapsulated at the source VTEP
```

## VTEP — VXLAN Tunnel Endpoint

A VTEP performs the encapsulation and decapsulation. In this design the **leaf
switches are the VTEPs**. The VTEP is addressed by a loopback (`vtep_loopback`),
which becomes the source/destination IP of the VXLAN tunnel in the underlay.

- Ingress VTEP: maps the host's VLAN to a VNI, encapsulates, and forwards toward
  the destination VTEP loopback.
- Egress VTEP: decapsulates and delivers the frame on the local VLAN.

## Anycast VTEP for MLAG

Within an MLAG pair both switches share the same VTEP loopback (an **anycast
VTEP**). Remote VTEPs see a single tunnel endpoint regardless of which physical
switch forwards the traffic, which keeps the overlay stable during a member
failure.

## EVPN as the Control Plane

Rather than flood-and-learn, this design uses **EVPN** to distribute MAC and
MAC/IP reachability. The ingress VTEP learns where a remote MAC lives from EVPN
Type-2 routes and builds the tunnel directly — no data-plane flooding required
for known unicast.

## BUM Traffic

Broadcast, Unknown-unicast, and Multicast (BUM) traffic is handled either by:

- **Head-end / ingress replication** — the source VTEP unicasts a copy to each
  remote VTEP in the VNI (default, no underlay multicast needed), or
- **Underlay multicast** — VTEPs join a shared multicast group per VNI.

See [Multicast Overview](MulticastOverview.md) and
[BUM Traffic Optimization](BUMTrafficOptimization.md).

## Key Fields

| Field | Sheet | Purpose |
|-------|-------|---------|
| vtep_loopback | Leaf | Source IP of all VXLAN tunnels for the leaf |
| vni | VRFs / VLANs | Segment identifier carried in the VXLAN header |
