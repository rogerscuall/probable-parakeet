# Service Insertion Overview

## Purpose

Service Insertion integrates stateful network services — firewalls, load
balancers, IDS/IPS — into the fabric without disrupting the underlay or overlay.
It defines how traffic is steered through a service node before reaching its
destination.

## Insertion Methods

| Mode | Description |
|------|-------------|
| routed | L3 insertion using PBR or static/route-leaking; the service is a routed hop between VRFs or subnets |
| transparent | L2 insertion via VLAN stitching; the service bridges two segments and is invisible at L3 |
| one_arm | The service connects on a single arm; traffic is policy-routed to it and returns asymmetrically |

The `insertion_mode` column captures which method each service uses.

## Service Types

| service_type | Examples |
|--------------|----------|
| firewall | Palo Alto, Cisco FTD, Fortinet |
| load_balancer | F5, Citrix ADC, A10 |
| ids_ips | Cisco Firepower, Snort |
| proxy | SSL/TLS inspection, forward/reverse proxies |
| other | Any appliance not covered above |

## Steering Traffic

Service nodes attach to the fabric on a **service leaf** and live in (or between)
specific VRFs. Traffic is steered using:

- **Inter-VRF routing** through the service for tenant-to-tenant flows.
- **Policy-based routing (PBR)** to force selected flows through the appliance.
- **Default-route injection** so a VRF's egress always transits the service.

## Design Considerations

- **High availability** — deploy clustered/active-active service nodes and plan
  failover so flows are not blackholed.
- **Traffic symmetry** — stateful devices require both directions of a flow to
  traverse the same node; design routing to guarantee this.
- **Throughput** — size appliances for the aggregate inspected bandwidth.
- **Service chaining** — order multiple appliances deterministically.

## Configuration Reference

Service data is entered in the **ServiceInsertion** sheet.

| Field | Description | Required |
|-------|-------------|----------|
| service_name | Unique service identifier | Yes |
| service_type | firewall / load_balancer / ids_ips / proxy / other | Yes |
| insertion_mode | routed / transparent / one_arm | Yes |
| vrf | VRF the service is inserted into | Yes |

## Related

- [Firewall Integration](FirewallIntegration.md)
- [Load Balancer Integration](LoadBalancerIntegration.md)
