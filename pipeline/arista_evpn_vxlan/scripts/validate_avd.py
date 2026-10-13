#!/usr/bin/env python3
"""Validate resolved Ansible host variables against the AVD eos_designs schema."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def fabric_hosts(inventory, group, visiting=None):
    """Include hosts in descendant groups without validating unrelated hosts."""
    visiting = set() if visiting is None else visiting
    if group in visiting:
        raise ValueError(f"Inventory group cycle involving {group!r}")
    if group not in inventory:
        raise ValueError(f"Inventory group {group!r} was not found")
    visiting.add(group)
    hosts = set(inventory[group].get("hosts", []))
    for child in inventory[group].get("children", []):
        hosts.update(fabric_hosts(inventory, child, visiting))
    visiting.remove(group)
    return hosts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="Ansible inventory YAML file")
    parser.add_argument("--fabric", default="FABRIC", help="Fabric inventory group")
    args = parser.parse_args()

    if not args.inventory.is_file():
        parser.error(f"Inventory file not found: {args.inventory}")

    try:
        from pyavd import validate_inputs
    except ImportError:
        print("Install dependencies first: python -m pip install -r requirements.txt", file=sys.stderr)
        return 1

    try:
        result = subprocess.run(
            ["ansible-inventory", "-i", str(args.inventory), "--list"],
            capture_output=True, text=True, check=True,
        )
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        inventory = json.loads(result.stdout)
        hosts = fabric_hosts(inventory, args.fabric)
        if not hosts:
            raise ValueError(f"Inventory group {args.fabric!r} has no hosts")

        failed = False
        hostvars = inventory.get("_meta", {}).get("hostvars", {})
        for host in sorted(hosts):
            inputs = dict(hostvars.get(host, {}))
            inputs["inventory_hostname"] = host
            validation = validate_inputs(inputs)
            for warning in validation.deprecation_warnings:
                print(f"{host}: {warning}", file=sys.stderr)
            for error in validation.validation_errors:
                print(f"{host}: {error}", file=sys.stderr)
            failed = failed or validation.failed

        if failed:
            return 1
        print(f"AVD validation passed for {len(hosts)} host(s) in {args.fabric}.")
        return 0
    except subprocess.CalledProcessError as error:
        print(error.stderr or str(error), file=sys.stderr)
    except (OSError, ValueError) as error:
        print(f"AVD validation failed: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
