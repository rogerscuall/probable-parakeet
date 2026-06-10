# Arista EVPN VXLAN Design Content

This directory contains all content for the Arista EVPN VXLAN data center fabric
design documentation. The data model mirrors Arista AVD (Ansible Validated
Designs): the spreadsheet a user fills in maps 1:1 onto the AVD `inventory.yml`
and `group_vars/` structure.

## Content Structure

```
arista_evpn_vxlan/
├── markdown/           # Documentation markdown files
└── templates/          # Excel input template (main-template.xlsx)
```

> **Note:** This repo stores the template as `main-template.xlsx`. The
> application currently loads the template by the fixed filename
> `cloudwan_template.xlsx` under `templates/` (see `TemplateService` in the
> app), so the app-side copy keeps that name until the loader is made
> design-type aware.

## Design Principles

The template requests the **minimum** input needed to render a full AVD
project. Anything AVD can derive is never asked for:

- Per-device loopback, VTEP, and router-id addresses — carved from the
  node-type pools using each device's `id`
- Management mask and Ansible host address — `mgmt_ip` is asked once per
  device, combined with a single fabric-wide `mgmt_prefix_length`
- VRF route distinguishers / route targets — derived from VNIs
- Per-VLAN VNIs — derived from the tenant `mac_vrf_vni_base` + `vlan_id`
- Uplink/downlink interface allocation — AVD `default_interfaces`, with an
  optional per-device `uplink_switch_interfaces` override

## Markdown Files

| File | Label(s) | Description |
|------|----------|-------------|
| BGPAddressFamilies.md | fabric | Underlay/overlay address families |
| EVPNRouteTypes.md | fabric | EVPN route types (2/3/4/5) |
| SpineLayerOverview.md | topology | Spine backbone and L3 design principles |
| LeafLayerOverview.md | topology | Leaf/VTEP roles and MLAG redundancy |
| EVPNRouteReflectors.md | topology | EVPN control plane / route reflection |
| VXLANandVTEP.md | topology | VXLAN encapsulation and VTEP behavior |
| VRFsAndTenantIsolation.md | network_services | L3 tenant isolation, RD/RT |
| VLANtoVXLANMapping.md | network_services | VLAN↔VNI mapping strategy |
| AnycastGateway.md | network_services | Distributed anycast gateway / symmetric IRB |
| ConnectedEndpoints.md | connected_endpoints | Endpoint adapters, port-channels, MLAG attachment |
| MonitoringOverview.md | cloudvision | Telemetry options and what to watch |
| StreamingTelemetry.md | cloudvision | gNMI/OpenConfig streaming telemetry |

The remaining markdown files (SuperSpine\*, Border\*, ServiceInsertion,
Firewall/LoadBalancer, Multicast/BUM, BGPPolicyAndFiltering) are reference
material not currently linked to a label; they are kept for future labels.

## XLSX Template Sheets

| Sheet | Label | Key Columns | AVD Source |
|-------|-------|-------------|------------|
| Fabric | fabric | fabric_name, underlay/overlay_routing_protocol, mgmt_gateway, mgmt_prefix_length, p2p_uplinks_mtu, dns_server, ntp_server | `group_vars/FABRIC.yml`, mgmt gateway from the DC group vars |
| NodeTypes | topology | node_type, platform, bgp_as, loopback/vtep/uplink/mlag pools, virtual_router_mac_address, spanning_tree\*, uplink_switches | `node_type.defaults` blocks in the DC group vars |
| Devices | topology | hostname, node_type, id, mgmt_ip, node_group, bgp_as, uplink_switch_interfaces | `inventory.yml` hosts + `nodes`/`node_groups` definitions |
| Tenants | network_services | tenant_name, mac_vrf_vni_base | `tenants[]` in NETWORK_SERVICES |
| VRFs | network_services | tenant, vrf_name, vrf_vni, vtep_diagnostic\* | `tenants[].vrfs[]` |
| VLANs | network_services | tenant, vlan_id, name, vrf, ip_address_virtual | `vrfs[].svis[]` (vrf set) and `l2vlans[]` (vrf blank) |
| ConnectedEndpoints | connected_endpoints | endpoint_name, endpoint_ports, switches, switch_ports, vlans, mode, port_channel_mode, spanning_tree_portfast | `servers[].adapters[]` in CONNECTED_ENDPOINTS |
| CloudVision | cloudvision | cv_server, cv_vrf | `cv_servers` / `daemon_terminattr` in FABRIC.yml |

## Labels

Labels are defined in `config/labels/arista_evpn_vxlan.yaml` and determine which
markdown files and template sheets are included based on user selections.

## Regenerating the Template

The template is generated from the label YAML so the two never drift:

```bash
python3 scripts/build_evpn_template.py \
  config/labels/arista_evpn_vxlan.yaml \
  content/arista_evpn_vxlan/templates/main-template.xlsx
```
