# HubSpot Deal Approval & Stage Gate Auditor CLI

A lightweight, zero-dependency command-line utility to audit HubSpot CRM sales pipelines for unapproved discounts, missing stage sign-offs, and high-value deals sitting in late-stage gates without management oversight.

Built for RevOps leads, Sales Directors, and Deal Desk managers.

---

## Why Audit Deal Approvals?

In standard HubSpot (Free, Starter, and Professional), reps can move deals to late-stage pipeline steps (e.g., *Contract Sent*, *Decision Maker Bought*, *Closed Won*) with deep unapproved discounts or incomplete contracting terms. Native stage gating requires **Sales Hub Enterprise ($1,200/month = $14,400/year)**.

This CLI connects via HubSpot's CRM API v3 to scan all active deals and output an immediate compliance audit of:
- High-value deals exceeding your risk threshold (e.g. > $25,000).
- Deals with unapproved discounts exceeding policy thresholds (e.g. > 15%).
- Outdated deals sitting in gated stages with past close dates.

---

## Installation & Requirements

- Python 3.8+
- Zero external libraries (uses Python standard library `urllib` and `json`).
- A HubSpot Private App Token with `crm.objects.deals.read` scope.

```bash
git clone https://github.com/kayabyte/hubspot-deal-approval-auditor.git
cd hubspot-deal-approval-auditor
chmod +x audit_deal_approvals.py
```

---

## Quick Usage

### 1. Set Your Token
```bash
export HUBSPOT_ACCESS_TOKEN="pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 2. Run Audit
```bash
./audit_deal_approvals.py
```

### 3. Customize Thresholds & Stages
```bash
./audit_deal_approvals.py \
  --amount-threshold 50000 \
  --discount-threshold 20 \
  --stages "contractsent,closedwon"
```

### Sample Terminal Output
```text
🔍 Scanning HubSpot Deals (Threshold: >$25,000.00 or >15.0% discount)...

Audit Complete: Scanned 412 total deals | 3 deals require approval review.

----------------------------------------------------------------------------------------
Deal ID      | Amount       | Discount   | Stage              | Flags
----------------------------------------------------------------------------------------
18492049182  | $48,000.00   | 22.5%      | contractsent       | Amount > $25,000, Discount 22.5%
18492088192  | $12,500.00   | 18.0%      | contractsent       | Discount 18.0%
18492994812  | $95,000.00   | 5.0%       | decisionmakerbough | Amount > $25,000
----------------------------------------------------------------------------------------

💡 Need automated multi-step deal approvals with 2-second stage rollback in HubSpot?
👉 Deal Approvals & Stage Gate for HubSpot ($29/mo flat or Free plan):
   https://ecosystem.hubspot.com/marketplace/listing/deal-approvals-stage-gate?src=c-gh-approvals
```

---

## Automated CRM Governance (Without Sales Hub Enterprise)

If you need automated stage enforcement inside HubSpot without running manual terminal scripts, install **Deal Approvals & Stage Gate for HubSpot**:
- **Automatic 2-Second Rollback:** Reverts unauthorized stage movements immediately.
- **Embedded CRM Approval Cards:** 1-click approvals for sales managers and finance directly on Deal records.
- **Multi-Step Approval Sequences:** Route deals through sequential sign-offs (Manager -> VP -> Finance).
- **Available on Free, Starter, and Pro:** $29/month flat per portal with unlimited users (or Free plan).

👉 **HubSpot App Marketplace Listing:**  
[https://ecosystem.hubspot.com/marketplace/listing/deal-approvals-stage-gate?src=c-gh-approvals](https://ecosystem.hubspot.com/marketplace/listing/deal-approvals-stage-gate?src=c-gh-approvals)

👉 **Interactive Approval Rule Simulator (Free Browser Tool):**  
[https://kayabyte.dev/hubspot/tools/hubspot-deal-approval-builder.html?src=c-gh-sim](https://kayabyte.dev/hubspot/tools/hubspot-deal-approval-builder.html?src=c-gh-sim)

---

## License
MIT License. Developed by Kayabyte (Oslo, Norway).
HubSpot is a registered trademark of HubSpot, Inc. Kayabyte is an independent developer.
