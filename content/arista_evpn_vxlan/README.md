# Arista EVPN VXLAN Design Content

This directory contains all content for the Arista EVPN VXLAN data center fabric
design documentation.

## Content Structure

```
arista_evpn_vxlan/
├── markdown/           # Documentation markdown files
└── templates/          # Excel input template (cloudwan_template.xlsx)
```

> **Note:** The application currently loads the template by the fixed filename
> `cloudwan_template.xlsx` under `templates/` (see `TemplateService` in the app).
> Keep that filename until the loader is made design-type aware.

## Markdown Files

| File | Label(s) | Description |
|------|----------|-------------|
| SuperSpineOverview.md | super_spine | Super Spine tier role and when to use it |
| SuperSpineDesignPatterns.md | super_spine | Topology, ASN, and scaling patterns |
| SpineLayerOverview.md | spine | Spine backbone and L3 design principles |
| EVPNRouteReflectors.md | spine | EVPN control plane / route reflection |
| LeafLayerOverview.md | leaf | Leaf/VTEP roles and MLAG redundancy |
| VXLANandVTEP.md | leaf | VXLAN encapsulation and VTEP behavior |
| AnycastGateway.md | leaf | Distributed anycast gateway / symmetric IRB |
| VRFsAndTenantIsolation.md | vrfs_vlans | L3 tenant isolation, RD/RT |
| VLANtoVXLANMapping.md | vrfs_vlans | VLAN↔VNI mapping strategy |
| BorderLeafArchitecture.md | border | External/DCI gateway patterns |
| DataCenterInterconnect.md | border | EVPN Multi-Site and DCI transport |
| ServiceInsertionOverview.md | service_insertion | Service insertion modes and steering |
| FirewallIntegration.md | service_insertion | Firewall insertion patterns |
| LoadBalancerIntegration.md | service_insertion | Load balancer deployment modes |
| BGPAddressFamilies.md | bgp_address_family | Underlay/overlay address families |
| EVPNRouteTypes.md | bgp_address_family | EVPN route types (2/3/4/5) |
| BGPPolicyAndFiltering.md | bgp_address_family | Route policy and RT filtering |
| MulticastOverview.md | multicast | BUM replication modes |
| BUMTrafficOptimization.md | multicast | Reducing and optimizing BUM traffic |
| MonitoringOverview.md | monitoring | Telemetry options and what to watch |
| StreamingTelemetry.md | monitoring | gNMI/OpenConfig streaming telemetry |

## XLSX Template Sheets

| Sheet | Label | Key Columns |
|-------|-------|-------------|
| SuperSpine | super_spine | hostname, asn, loopback_ip, router_id |
| Spine | spine | hostname, asn, loopback_ip, role |
| Leaf | leaf | hostname, asn, vtep_loopback, mlag_domain_id, leaf_type |
| VRFs | vrfs_vlans | vrf_name, vni, route_distinguisher |
| VLANs | vrfs_vlans | vlan_id, vni, anycast_gateway, vrf |
| BorderLeaf | border | hostname, border_type, external_asn |
| ServiceInsertion | service_insertion | service_name, service_type, insertion_mode, vrf |
| BGPAddressFamily | bgp_address_family | device_hostname, address_family, route_reflector_client |
| Multicast | multicast | replication_mode |
| Monitoring | monitoring | telemetry_type |

## Labels

Labels are defined in `config/labels/arista_evpn_vxlan.yaml` and determine which
markdown files and template sheets are included based on user selections.

## Regenerating the Template

The template is generated from the label YAML so the two never drift:

```bash
python3 scripts/build_evpn_template.py \
  config/labels/arista_evpn_vxlan.yaml \
  content/arista_evpn_vxlan/templates/cloudwan_template.xlsx
```
