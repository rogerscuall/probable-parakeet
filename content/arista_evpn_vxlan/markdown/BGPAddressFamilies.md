# BGP Address Families

## Overview

BGP carries both the underlay and the overlay in this design. Address families
separate the different kinds of reachability so each can be advertised, filtered,
and policed independently.

## Supported Address Families

| address_family | Role |
|----------------|------|
| evpn | L2VPN EVPN — MAC, MAC/IP, and IP-prefix routes for the overlay |
| ipv4_unicast | Underlay reachability and IPv4 VRF routing |
| ipv6_unicast | IPv6 underlay and overlay support |
| vpnv4 | MPLS L3VPN integration (IPv4) at the DCI/edge |
| vpnv6 | MPLS L3VPN integration (IPv6) at the DCI/edge |

The `address_family` column records which families a device activates.

## Underlay vs. Overlay

- **Underlay** (`ipv4_unicast` / `ipv6_unicast`): advertises loopbacks and
  point-to-point links so VTEPs can reach each other. Typically eBGP per the
  Clos ASN plan.
- **Overlay** (`evpn`): distributes host and prefix reachability between VTEPs,
  reflected by the spines. The EVPN next hop is the originating VTEP loopback.

## Route Reflector Clients

The `route_reflector_client` column flags whether a device peers as a client of
the EVPN route reflectors (the spines). Leaves are usually RR clients; spines are
the reflectors. See [EVPN Route Reflectors](EVPNRouteReflectors.md).

## Resilience Features

- **Graceful Restart / NSR** — preserve forwarding during control-plane events.
- **BFD** — sub-second neighbor failure detection on underlay and overlay peers.
- **Maximum-paths / ECMP** — install all equal-cost underlay paths.

## Configuration Reference

Per-device address-family data is entered in the **BGPAddressFamily** sheet.

| Field | Description | Required |
|-------|-------------|----------|
| device_hostname | Device the address family applies to | Yes |
| address_family | evpn / ipv4_unicast / ipv6_unicast / vpnv4 / vpnv6 | Yes |
| route_reflector_client | Whether the device is an RR client (yes/no) | No |

## Related

- [EVPN Route Types](EVPNRouteTypes.md)
- [BGP Policy and Filtering](BGPPolicyAndFiltering.md)
