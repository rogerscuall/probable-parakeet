#!/usr/bin/env python3
"""
Generate CloudWAN policy document from CSV configuration.

Usage:
    python generate_policy.py <data_directory> --output <output_file>
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def load_csv(filepath: Path) -> list:
    """Load CSV file as list of dictionaries."""
    if not filepath.exists():
        return []

    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))


def generate_policy(data_dir: Path) -> dict:
    """Generate CloudWAN policy from CSV data."""

    # Load data
    core_network = load_csv(data_dir / 'corenetwork.csv')
    segments = load_csv(data_dir / 'segments.csv')
    segment_sharing = load_csv(data_dir / 'segmentsharing.csv')
    static_routes = load_csv(data_dir / 'staticroutes.csv')
    nfgs = load_csv(data_dir / 'networkfunctiongroups.csv')
    nfg_send_via = load_csv(data_dir / 'nfgsendvia.csv')
    nfg_send_to = load_csv(data_dir / 'nfgsendto.csv')

    # Build policy structure
    policy = {
        'version': '2021.12',
        'core-network-configuration': {
            'vpn-ecmp-support': True,
            'asn-ranges': [],
            'edge-locations': []
        },
        'segments': [],
        'segment-actions': [],
        'network-function-groups': []
    }

    # Process core network configuration
    regions = set()
    asn_values: list[int] = []
    inside_cidr_blocks: list[str] = []

    for row in core_network:
        if row.get('region'):
            regions.add(row['region'])
        if row.get('asn'):
            asn_values.append(int(row['asn']))
        if row.get('inside_cidr_blocks'):
            inside_cidr_blocks.extend(
                cidr.strip() for cidr in row['inside_cidr_blocks'].split(',')
            )

    # Build ASN range from min to max+1 (AWS requires range end to be exclusive)
    if asn_values:
        min_asn = min(asn_values)
        max_asn = max(asn_values)
        policy['core-network-configuration']['asn-ranges'] = [f"{min_asn}-{max_asn + 1}"]

    # Deduplicate and set inside CIDR blocks
    if inside_cidr_blocks:
        policy['core-network-configuration']['inside-cidr-blocks'] = list(dict.fromkeys(inside_cidr_blocks))

    for region in regions:
        policy['core-network-configuration']['edge-locations'].append({
            'location': region
        })

    # Process segments
    for row in segments:
        segment = {
            'name': row.get('name', ''),
            'description': row.get('description', ''),
            'isolate-attachments': row.get('isolate_attachments', 'no').lower() == 'yes',
            'require-attachment-acceptance': row.get('require_attachment_acceptance', 'no').lower() == 'yes'
        }
        policy['segments'].append(segment)

    # Process segment sharing
    for row in segment_sharing:
        if row.get('sharing_enabled', '').lower() == 'yes':
            policy['segment-actions'].append({
                'action': 'share',
                'mode': 'attachment-route',
                'segment': row.get('segment_a', ''),
                'share-with': row.get('segment_b', '')
            })

    # Process network function groups
    for row in nfgs:
        nfg = {
            'name': row.get('name', ''),
            'description': row.get('description', ''),
            'require-attachment-acceptance': row.get('require_attachment_acceptance', 'no').lower() == 'yes'
        }
        policy['network-function-groups'].append(nfg)

    # Process send-via routes
    for row in nfg_send_via:
        policy['segment-actions'].append({
            'action': 'send-via',
            'segment': row.get('segment_a', ''),
            'via': {
                'network-function-groups': [row.get('nfg', '')]
            },
            'destination-cidr-blocks': ['0.0.0.0/0']  # Default
        })

    # Process send-to routes
    for row in nfg_send_to:
        policy['segment-actions'].append({
            'action': 'send-to',
            'segment': row.get('segment', ''),
            'via': {
                'network-function-groups': [row.get('nfg', '')]
            }
        })

    # Remove empty optional fields from policy
    if not policy['segment-actions']:
        del policy['segment-actions']
    if not policy['network-function-groups']:
        del policy['network-function-groups']
    if not policy['segments']:
        del policy['segments']

    return policy


def main():
    parser = argparse.ArgumentParser(description='Generate CloudWAN policy')
    parser.add_argument('data_dir', help='Directory containing CSV files')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Directory not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    policy = generate_policy(data_dir)

    with open(args.output, 'w') as f:
        json.dump(policy, f, indent=2)

    print(f"Policy generated: {args.output}")


if __name__ == '__main__':
    main()
