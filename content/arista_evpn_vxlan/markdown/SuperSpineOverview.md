# Super Spine Layer Overview

## Introduction

The Super Spine layer is the highest tier of connectivity in a multi-pod or
large-scale data center fabric. It interconnects multiple pod-level spine
layers and provides Data Center Interconnect (DCI) capabilities, allowing the
fabric to scale horizontally beyond the port density of a single spine tier.

## When to Use a Super Spine

A Super Spine tier is introduced when a single pair (or set) of spines can no
longer provide enough uplink capacity for the required number of leaf switches,
or when the design spans multiple physical pods, rooms, or buildings.

- **Multi-pod deployments** (typically 5+ pods)
- **Data center interconnect (DCI)** across rooms or sites
- **Scalable campus or metro fabric** designs
- **High-availability tier** for critical infrastructure

For small, single-pod fabrics the Super Spine is optional and the label can be
left unselected. When present, every pod spine connects northbound to every
Super Spine node, forming a 5-stage Clos topology.

## Role in the Fabric

```
        +-------------+        +-------------+
        | Super Spine |        | Super Spine |   <-- this layer
        +------+------+        +------+------+
               |   \          /   |
               |    \        /    |
        +------+--+  +------+--+   ...
        |  Spine  |  |  Spine  |        (per-pod spine tier)
        +---------+  +---------+
```

The Super Spine participates only in the **underlay** (IP transport). It is a
pure Layer 3 device running eBGP (or OSPF) toward the pod spines and does not
hold any VXLAN VTEP or EVPN overlay state. Keeping the Super Spine overlay-free
maximizes its forwarding scale and simplifies troubleshooting.

## Hardware Considerations

- High-density spine-class platforms (e.g., 7800 series) for port count
- Deep buffers where many-to-one (incast) traffic is expected
- Redundant supervisors and power for the availability this tier demands

## Configuration Reference

Data for this layer is entered in the **SuperSpine** sheet of the template.

| Field | Description | Required |
|-------|-------------|----------|
| hostname | Unique device identifier | Yes |
| asn | BGP autonomous system number for the underlay | Yes |
| loopback_ip | Router loopback used for BGP/underlay reachability | Yes |
| router_id | BGP router-id (typically the loopback) | Yes |

See [Super Spine Design Patterns](SuperSpineDesignPatterns.md) for topology and
ASN allocation guidance.
