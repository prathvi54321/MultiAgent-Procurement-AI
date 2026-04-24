import json
import os

def intake_agent(query):
    return {"item": "laptop", "quantity": 20, "budget": 1000000}

def vendor_agent():
    import os
    import json

    path = os.path.join(os.path.dirname(__file__), "data", "vendors.json")

    with open(path, "r") as f:
        return json.load(f)

def quote_agent(vendors):
    return sorted(vendors, key=lambda x: x["price"])

def compliance_agent(vendors):
    return [v for v in vendors if v["rating"] >= 4.4]

def approval_agent(total_cost):
    if total_cost < 500000:
        return "Auto Approved"
    return "Manager Approval Required"

def po_agent(best_vendor, quantity):
    total = best_vendor["price"] * quantity
    return f"""
Purchase Order:
Vendor: {best_vendor['vendor']}
Quantity: {quantity}
Total Cost: ₹{total}
"""