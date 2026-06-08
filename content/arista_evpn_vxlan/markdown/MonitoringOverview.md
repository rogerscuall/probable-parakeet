# Monitoring and Telemetry Overview

## Purpose

Operating an EVPN VXLAN fabric requires real-time visibility into underlay
health, overlay state, and host reachability. This design lets you record which
telemetry mechanisms each device uses so the generated documentation and
automation provision them consistently.

## Telemetry Options

| telemetry_type | Description |
|----------------|-------------|
| streaming_telemetry | Push-based gNMI/OpenConfig streaming for low-latency state |
| sflow | Sampled traffic export for traffic-pattern analysis |
| netflow | Flow records (NetFlow/IPFIX) for flow-level accounting |
| snmp | Polling-based metrics for legacy NMS integration |
| syslog | Event and log stream for correlation and alerting |

The `telemetry_type` column captures the mechanism selected for each device or
the fabric.

## What to Watch in an EVPN VXLAN Fabric

- **Underlay**: BGP/OSPF adjacencies, ECMP path counts, BFD state, link errors.
- **Overlay**: EVPN session state, route counts (Type-2/Type-5), VTEP peer list.
- **Host plane**: MAC/ARP table size, host mobility (sequence-number churn).
- **BUM**: replication volume per VNI (see [BUM Traffic Optimization](BUMTrafficOptimization.md)).

## Tooling

| Category | Examples |
|----------|----------|
| Arista-native | CloudVision Portal (CVP) |
| Generic NMS | SolarWinds, PRTG, LibreNMS |
| Analytics | Splunk, ELK |
| Metrics/dashboards | Prometheus, Grafana |

## Common Scenarios

- Troubleshooting EVPN convergence and host-move issues
- Capacity planning and traffic engineering
- Security monitoring and anomaly detection
- Compliance auditing and reporting

## Related

- [Streaming Telemetry](StreamingTelemetry.md)
