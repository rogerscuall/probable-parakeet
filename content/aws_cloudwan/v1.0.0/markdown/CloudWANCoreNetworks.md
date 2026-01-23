# Core Network Configuration

## Overview

The Core Network is the foundational component of your AWS Cloud WAN deployment. It provides the global routing infrastructure that connects all your network segments and attachments.

## Configuration Parameters

### Region Selection

Select the AWS Regions where your Core Network will have edge locations. Consider:

- Current workload locations
- Disaster recovery requirements
- Latency requirements for inter-region traffic
- Cost implications of cross-region data transfer

### ASN (Autonomous System Number)

The ASN is used for BGP peering with:

- On-premises networks
- Third-party network appliances
- AWS Direct Connect gateways

**Recommended Ranges:**
- Private ASN: 64512-65534 (16-bit) or 4200000000-4294967294 (32-bit)
- Public ASN: Use your organization's registered ASN if connecting to public networks

### Inside CIDR Blocks

Inside CIDR blocks define the IP address space used internally by Cloud WAN for:

- Core Network Edge connections
- Transit between segments
- Internal routing

**Best Practices:**
- Use RFC 1918 private address space
- Avoid overlap with existing VPC CIDR blocks
- Plan for future expansion

## Example Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Regions | us-east-1, us-west-2, eu-west-1 | Primary regions |
| ASN | 64512 | Private ASN |
| Inside CIDR | 10.255.0.0/16 | Non-overlapping range |
