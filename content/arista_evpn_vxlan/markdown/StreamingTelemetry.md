# Streaming Telemetry

## Why Streaming Telemetry

Traditional SNMP polling is too slow and coarse for a modern fabric. **Streaming
telemetry** pushes state changes from the device as they happen, using a
structured data model. This gives near-real-time visibility into convergence,
host moves, and link events that polling would miss.

## Standards and Transport

| Component | Role |
|-----------|------|
| OpenConfig | Vendor-neutral YANG data models for config and state |
| gNMI | gRPC-based transport for subscribe/get/set operations |
| Subscriptions | `sample` (periodic) or `on-change` (event-driven) streams |

`on-change` subscriptions are ideal for state that matters immediately (BGP/EVPN
session up/down), while `sample` is suited to counters and utilization.

## What to Stream in an EVPN VXLAN Fabric

- BGP and EVPN neighbor state and route counts
- VXLAN VTEP peer list and tunnel state
- Interface counters, errors, and optics
- MAC/ARP table size and host-mobility events
- BFD session state for fast-failure visibility

## Collection and Analysis

- **CloudVision Portal (CVP)** consumes Arista streaming telemetry natively and
  provides state history ("time travel") for troubleshooting.
- Open-source pipelines: gNMI collector → time-series DB (Prometheus/InfluxDB) →
  Grafana dashboards.
- Stream to analytics platforms (Splunk, ELK) for correlation with logs.

## Best Practices

- Subscribe `on-change` for control-plane state, `sample` for counters.
- Establish baselines so anomaly detection is meaningful.
- Secure the telemetry channel (TLS, authenticated gRPC).
- Correlate telemetry with syslog for full event context.

## Related

- [Monitoring Overview](MonitoringOverview.md)
