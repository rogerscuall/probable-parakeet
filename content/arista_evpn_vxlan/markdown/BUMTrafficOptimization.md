# BUM Traffic Optimization

## What Is BUM Traffic

BUM = **B**roadcast, **U**nknown-unicast, and **M**ulticast. In a bridged
segment this traffic must reach every member. In a VXLAN overlay it must reach
every VTEP participating in the VNI, which — if unmanaged — wastes fabric
bandwidth and CPU.

## Reduce It at the Source

EVPN dramatically reduces BUM in the first place:

- **ARP/ND suppression** — leaves answer ARP locally from EVPN Type-2 state, so
  ARP broadcasts rarely cross the fabric.
- **No unknown-unicast flooding** — MAC reachability is learned via the control
  plane, so "unknown" unicast is largely eliminated. Many designs disable
  unknown-unicast flooding entirely.
- **Host route advertisement** — silent hosts can be advertised so traffic to
  them never floods.

## Then Optimize What Remains

For the residual broadcast/multicast, pick the replication mode that matches
scale (see [Multicast Overview](MulticastOverview.md)):

| Approach | Best for |
|----------|----------|
| Head-end replication | Small fabrics, simple underlay |
| Ingress replication | Medium fabrics, control-plane-built lists |
| Underlay multicast (PIM) | Large fabrics, high BUM volume |

## Operational Tips

- Monitor BUM volume per VNI; spikes often indicate ARP storms or loops.
- Keep VNIs scoped to the leaves that actually need them — fewer members means
  less replication.
- Validate that ARP suppression is active on all leaves serving a subnet.
- For multicast mode, confirm PIM neighbor and RP health as part of monitoring.

## Related

- [Multicast Overview](MulticastOverview.md)
- [VXLAN and VTEP](VXLANandVTEP.md)
- [Monitoring Overview](MonitoringOverview.md)
