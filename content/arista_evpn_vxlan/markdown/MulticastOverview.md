# Multicast Overview

## Why It Matters

VXLAN must deliver Broadcast, Unknown-unicast, and Multicast (BUM) traffic to all
VTEPs in a segment. How that replication happens has a large impact on fabric
efficiency and underlay complexity. This design lets you choose the replication
mode per fabric.

## Replication Modes

| replication_mode | How it works | Trade-off |
|------------------|--------------|-----------|
| head_end_replication | The source VTEP makes one unicast copy per remote VTEP | No underlay multicast needed; cost grows with VTEP count |
| ingress_replication | EVPN Type-3 builds the per-VNI replication list; source replicates to listed VTEPs | Control-plane driven, no underlay multicast; efficient at moderate scale |
| multicast | VTEPs join an underlay multicast group per VNI; underlay replicates | Most efficient at large scale; requires PIM in the underlay |

The `replication_mode` column selects the strategy for the fabric.

## Choosing a Mode

- **Small/medium fabrics**: head-end or ingress replication keep the underlay
  simple and are usually sufficient.
- **Large fabrics or heavy BUM**: underlay multicast (PIM) reduces replication
  load on source VTEPs at the cost of running multicast in the underlay.

## Underlay Multicast Building Blocks

When `multicast` is selected:

- **PIM Sparse Mode** for efficient distribution trees.
- **Anycast RP** for rendezvous-point redundancy.
- **SSM** where source-specific delivery is desired.

## Related

- [BUM Traffic Optimization](BUMTrafficOptimization.md)
- [VXLAN and VTEP](VXLANandVTEP.md)
