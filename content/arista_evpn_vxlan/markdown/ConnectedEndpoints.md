# Connected Endpoints

Connected endpoints describe how servers, storage arrays, firewalls, and other
devices attach to the leaf layer of the EVPN VXLAN fabric. They map directly to
the AVD `connected_endpoints` data model, which renders the leaf downlink
interfaces, port-channels, and MLAG configuration automatically.

## The Adapter Model

Each endpoint is described by one or more **adapters**. An adapter is a set of
physical links that share identical configuration — for example, a server's two
NICs cabled to both members of an MLAG leaf pair.

An adapter row defines three parallel, comma-separated lists that must have the
same length (one entry per physical link):

| List | Meaning | Example |
|------|---------|---------|
| `endpoint_ports` | Interface names on the endpoint itself | `Ethernet1,Ethernet2` |
| `switches` | Leaf switches terminating each link | `DC1-LEAF1A,DC1-LEAF1B` |
| `switch_ports` | Leaf interface used for each link | `Ethernet7,Ethernet7` |

The first entries of each list describe link one, the second entries link two,
and so on.

## VLANs and Port Mode

- `mode` selects `access` or `trunk` operation on the leaf ports.
- `vlans` lists the allowed VLANs for trunks (or the single access VLAN).
  Ranges and individual IDs can be combined: `11-13,21,25,31`.

VLAN IDs must already be defined in the **VLANs** sheet — the fabric only
transports segments that exist in the overlay.

## Port-Channels and MLAG

Setting `port_channel_mode` bundles the adapter links into a port-channel:

- `active` — LACP active (recommended)
- `passive` — LACP passive
- `on` — static bundle, no LACP

When the adapter spans both members of an MLAG leaf pair, AVD automatically
renders an **MLAG port-channel**, giving the endpoint an active/active
dual-homed attachment with no spanning-tree blocked links.

## Spanning Tree

`spanning_tree_portfast` should be set to `edge` for host-facing ports so they
transition to forwarding immediately. Use `network` only for ports facing
other bridges.

## What AVD Derives Automatically

- Port-channel numbering and interface descriptions
- MLAG configuration consistency across both leaf pair members
- Trunk group and VLAN pruning configuration
- Spanning-tree edge port protection settings
