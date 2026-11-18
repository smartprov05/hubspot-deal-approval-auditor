#!/usr/bin/env python3
"""
HubSpot Deal Approval & Stage Gate Auditor CLI
Audits HubSpot CRM deals in critical pipeline stages for missing approvals, high discounts, and governance violations.

Zero external dependencies - runs on standard Python 3.8+.
Part of the Kayabyte HubSpot Open-Source RevOps Toolkit.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

API_BASE = "https://api.hubapi.com"


def fetch_deals(token: str, properties: List[str], limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch deals with specified properties from HubSpot CRM API v3."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "kayabyte-deal-auditor/1.0"
    }
    
    url = f"{API_BASE}/crm/v3/objects/deals?limit={limit}&properties={','.join(properties)}"
    deals: List[Dict[str, Any]] = []
    
    while url:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                deals.extend(data.get("results", []))
                paging = data.get("paging", {}).get("next", {})
                url = paging.get("link")
        except urllib.error.HTTPError as err:
            sys.stderr.write(f"HubSpot API Error: {err.code} {err.reason}\n")
            if err.code == 401:
                sys.stderr.write("Invalid or expired Private App Access Token.\n")
            sys.exit(1)
        except Exception as ex:
            sys.stderr.write(f"Connection failed: {ex}\n")
            sys.exit(1)
            
    return deals


def main():
    parser = argparse.ArgumentParser(
        description="Audit HubSpot CRM deals for unapproved discounts and stage compliance."
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HUBSPOT_ACCESS_TOKEN"),
        help="HubSpot Private App Access Token (or set HUBSPOT_ACCESS_TOKEN env var)"
    )
    parser.add_argument(
        "--amount-threshold",
        type=float,
        default=25000.0,
        help="Flag deals above this amount ($ default: 25000)"
    )
    parser.add_argument(
        "--discount-threshold",
        type=float,
        default=15.0,
        help="Flag deals with discount percent above this threshold (% default: 15.0)"
    )
    parser.add_argument(
        "--stages",
        default="contractsent,decisionmakerbought,closedwon",
        help="Comma-separated stage internal names to audit"
    )

    args = parser.parse_args()

    if not args.token:
        sys.stderr.write("Error: HubSpot Private App Token required via --token or HUBSPOT_ACCESS_TOKEN.\n")
        sys.exit(1)

    target_stages = set(s.strip().lower() for s in args.stages.split(","))
    properties = ["dealname", "amount", "dealstage", "hs_discount_percentage", "closedate", "pipeline"]

    print(f"\n🔍 Scanning HubSpot Deals (Threshold: >${args.amount_threshold:,.2f} or >{args.discount_threshold}% discount)...")
    deals = fetch_deals(args.token, properties)

    flagged_deals = []
    for d in deals:
        props = d.get("properties", {})
        stage = (props.get("dealstage") or "").lower()
        
        # Check stage filter if specified
        if target_stages and stage not in target_stages:
            continue

        try:
            amount = float(props.get("amount") or 0.0)
        except ValueError:
            amount = 0.0

        try:
            discount = float(props.get("hs_discount_percentage") or 0.0)
        except ValueError:
            discount = 0.0

        flags = []
        if amount >= args.amount_threshold:
            flags.append(f"Amount > ${args.amount_threshold:,.0f}")
        if discount >= args.discount_threshold:
            flags.append(f"Discount {discount:.1f}%")

        if flags:
            flagged_deals.append({
                "id": d.get("id"),
                "name": props.get("dealname") or "Unnamed Deal",
                "stage": stage,
                "amount": amount,
                "discount": discount,
                "flags": ", ".join(flags)
            })

    print(f"\nAudit Complete: Scanned {len(deals)} total deals | {len(flagged_deals)} deals require approval review.\n")
    print("-" * 88)
    print(f"{'Deal ID':<12} | {'Amount':<12} | {'Discount':<10} | {'Stage':<18} | {'Flags'}")
    print("-" * 88)

    for item in flagged_deals:
        print(f"{item['id']:<12} | ${item['amount']:<11,.2f} | {item['discount']:<9.1f}% | {item['stage']:<18} | {item['flags']}")

    print("-" * 88)
    print("\n💡 Need automated multi-step deal approvals with 2-second stage rollback in HubSpot?")
    print("👉 Deal Approvals & Stage Gate for HubSpot ($29/mo flat or Free plan):")
    print("   https://ecosystem.hubspot.com/marketplace/listing/deal-approvals-stage-gate?src=c-gh-approvals\n")


if __name__ == "__main__":
    main()
