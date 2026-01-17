# Ingress Design

## Overview

This section covers patterns for handling inbound internet traffic to your Cloud WAN connected workloads.

## Ingress Patterns

### 1. Centralized Ingress

All internet traffic enters through a centralized ingress VPC:

```
Internet
    │
┌───┴───────────────────┐
│   Ingress VPC         │
│   - ALB/NLB           │
│   - WAF               │
│   - Shield            │
└───┬───────────────────┘
    │ Cloud WAN
    ├── Spoke VPC 1
    ├── Spoke VPC 2
    └── Spoke VPC N
```

**Advantages:**
- Centralized security controls
- Simplified certificate management
- Cost optimization through shared resources

### 2. Distributed Ingress

Each spoke VPC handles its own internet ingress:

```
Internet     Internet     Internet
    │            │            │
┌───┴───┐   ┌───┴───┐   ┌───┴───┐
│Spoke 1│   │Spoke 2│   │Spoke N│
│  ALB  │   │  ALB  │   │  ALB  │
└───┬───┘   └───┬───┘   └───┬───┘
    │           │           │
    └─────┬─────┴───────────┘
          │
      Cloud WAN
```

**Advantages:**
- Reduced latency
- Fault isolation
- Team autonomy

### 3. Regional Ingress Hubs

Balance between centralized and distributed:

```
Internet (us-east-1)    Internet (eu-west-1)
        │                       │
┌───────┴───────┐       ┌───────┴───────┐
│ Regional Hub  │       │ Regional Hub  │
│ us-east-1     │       │ eu-west-1     │
└───────┬───────┘       └───────┬───────┘
        │                       │
        └───────┬───────────────┘
                │
            Cloud WAN
```

## Selection Criteria

| Factor | Centralized | Distributed | Regional |
|--------|-------------|-------------|----------|
| Security | High control | Per-app | Regional control |
| Latency | Higher | Lowest | Moderate |
| Cost | Lower | Higher | Moderate |
| Complexity | Lower | Higher | Moderate |

## Recommendations

1. **Start Centralized**: Begin with centralized ingress and distribute as needed
2. **Use AWS WAF**: Apply web application firewall rules at the ingress point
3. **Enable Shield**: Protect against DDoS attacks
4. **Monitor Latency**: Use CloudWatch to identify when distribution is needed
