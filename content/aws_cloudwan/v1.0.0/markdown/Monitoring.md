# Monitoring

## Overview

AWS Cloud WAN integrates with Amazon CloudWatch to provide visibility into your network performance, health, and usage patterns.

## Available Metrics

### Attachment Metrics
- **BytesIn**: Bytes received by an attachment
- **BytesOut**: Bytes sent from an attachment
- **PacketsIn**: Packets received by an attachment
- **PacketsOut**: Packets sent from an attachment

### Core Network Metrics
- **AttachmentState**: Health status of attachments
- **ConnectionState**: Status of core network edge connections

## CloudWatch Dashboard

Create a custom dashboard to monitor:

1. **Traffic Overview**
   - Total bytes in/out across all attachments
   - Top talking attachments

2. **Health Status**
   - Attachment state summary
   - Failed attachment alerts

3. **Regional Distribution**
   - Traffic by region
   - Cross-region data transfer

## Alarms

Configure alarms for:

| Metric | Threshold | Action |
|--------|-----------|--------|
| AttachmentState | != Available | SNS notification |
| BytesIn | > baseline + 2 std dev | Investigation |
| ConnectionState | != Available | On-call page |

## Best Practices

1. **Baseline Metrics**: Establish normal traffic patterns before setting alarms
2. **Log Retention**: Configure appropriate log retention periods
3. **Cross-Account**: Use CloudWatch cross-account for centralized monitoring
4. **Automation**: Integrate with AWS Systems Manager for automated remediation
