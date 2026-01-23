#!/usr/bin/env python3
"""
Validate CloudWAN configuration data from CSV files.

Usage:
    python validate.py <data_directory>
"""

import argparse
import csv
import ipaddress
import os
import sys
from pathlib import Path


def validate_cidr(value: str) -> bool:
    """Validate CIDR notation."""
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def validate_asn(value: str) -> bool:
    """Validate ASN number."""
    try:
        asn = int(value)
        return 1 <= asn <= 4294967294
    except ValueError:
        return False


def validate_region(value: str) -> bool:
    """Validate AWS region."""
    valid_regions = {
        'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
        'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1',
        'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
        'sa-east-1', 'ca-central-1'
    }
    return value.lower() in valid_regions


def validate_core_network(data_dir: Path) -> list:
    """Validate CoreNetwork.csv"""
    errors = []
    csv_path = data_dir / 'corenetwork.csv'

    if not csv_path.exists():
        errors.append(f"Required file not found: {csv_path}")
        return errors

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            if 'region' in row and row['region']:
                if not validate_region(row['region']):
                    errors.append(f"CoreNetwork row {i}: Invalid region '{row['region']}'")

            if 'inside_cidr_blocks' in row and row['inside_cidr_blocks']:
                for cidr in row['inside_cidr_blocks'].split(','):
                    if not validate_cidr(cidr.strip()):
                        errors.append(f"CoreNetwork row {i}: Invalid CIDR '{cidr.strip()}'")

            if 'asn' in row and row['asn']:
                if not validate_asn(row['asn']):
                    errors.append(f"CoreNetwork row {i}: Invalid ASN '{row['asn']}'")

    return errors


def validate_segments(data_dir: Path) -> list:
    """Validate Segments.csv"""
    errors = []
    csv_path = data_dir / 'segments.csv'

    if not csv_path.exists():
        return errors  # Optional file

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            if not row.get('name'):
                errors.append(f"Segments row {i}: Missing required field 'name'")

            if 'edge_locations' in row and row['edge_locations']:
                for region in row['edge_locations'].split(','):
                    if not validate_region(region.strip()):
                        errors.append(f"Segments row {i}: Invalid region '{region.strip()}'")

    return errors


def main():
    parser = argparse.ArgumentParser(description='Validate CloudWAN configuration')
    parser.add_argument('data_dir', help='Directory containing CSV files')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Directory not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    all_errors = []
    all_errors.extend(validate_core_network(data_dir))
    all_errors.extend(validate_segments(data_dir))

    if all_errors:
        print("Validation errors found:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Validation passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
