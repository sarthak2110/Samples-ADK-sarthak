import asyncio
import datetime
import json
import logging
import os
import random
import uuid
from typing import Optional

from fastmcp import FastMCP

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize MCP Server
mcp = FastMCP("Customer Data MCP Server 👤")

# Sample pools for mock data generation
FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Casey", "Avery"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
DOMAINS = ["example.com", "corp.net", "techhub.io", "cloudscale.org", "saasapp.com"]
TIERS = ["Free", "Starter", "Pro", "Enterprise"]
STATUSES = ["Active", "Inactive", "Suspended", "Pending Verification"]
COUNTRIES = ["US", "CA", "GB", "DE", "IN", "AU", "FR", "JP"]
PRODUCT_CATEGORIES = ["Cloud Hosting", "Analytics Suite", "AI API Credits", "Database Storage", "Security Add-on"]


def _generate_mock_customer(customer_id: Optional[str] = None) -> dict:
    """Helper to generate a single customer record."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    cid = customer_id or f"CUST-{uuid.uuid4().hex[:8].upper()}"
    created_days_ago = random.randint(10, 1200)
    created_date = datetime.date.today() - datetime.timedelta(days=created_days_ago)

    return {
        "customer_id": cid,
        "name": f"{first} {last}",
        "email": f"{first.lower()}.{last.lower()}@{random.choice(DOMAINS)}",
        "tier": random.choice(TIERS),
        "status": random.choice(STATUSES),
        "country": random.choice(COUNTRIES),
        "lifetime_value_usd": round(random.uniform(50.0, 15000.0), 2),
        "monthly_recurring_revenue": round(random.uniform(10.0, 1200.0), 2),
        "member_since": created_date.isoformat(),
        "recent_purchases": [
            {
                "order_id": f"ORD-{random.randint(10000, 99999)}",
                "product": random.choice(PRODUCT_CATEGORIES),
                "amount_usd": round(random.uniform(20.0, 500.0), 2),
                "timestamp": (datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(1, 30))).isoformat() + "Z"
            }
            for _ in range(random.randint(1, 3))
        ]
    }


@mcp.tool()
def get_random_customer(customer_id: Optional[str] = None) -> str:
    """Fetches details for a customer.

    If a customer_id is provided, generates mock data mapped to that ID;
    otherwise, generates a brand-new random customer.

    Args:
        customer_id (str, optional): The ID of the customer (e.g., 'CUST-A1B2C3D4').

    Returns:
        str: JSON string containing customer details.
    """
    try:
        logger.info(f"Generating customer details (Customer ID: {customer_id or 'Random'})")
        customer = _generate_mock_customer(customer_id)
        return json.dumps(customer, indent=2)
    except Exception as e:
        logger.exception("An error occurred while generating customer profile")
        return json.dumps({"error": "Internal server error", "details": str(e)})


@mcp.tool()
def get_random_customer_batch(count: int = 5, tier: Optional[str] = None) -> str:
    """Generates a batch list of random customer records.

    Args:
        count (int): Number of customer records to generate (1-50, default is 5).
        tier (str, optional): Filter generated customers by tier ('Free', 'Starter', 'Pro', 'Enterprise').

    Returns:
        str: JSON string containing an array of customer profiles.
    """
    if count < 1 or count > 50:
        return json.dumps({"error": "Count must be between 1 and 50."})

    logger.info(f"Generating batch of {count} customers (Filtered Tier: {tier})")
    
    customers = []
    for _ in range(count):
        cust = _generate_mock_customer()
        if tier and tier.capitalize() in TIERS:
            cust["tier"] = tier.capitalize()
        customers.append(cust)

    return json.dumps({"total": len(customers), "customers": customers}, indent=2)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🚀 Customer MCP server started on port {port}")
    
    # Run the server using Streamable HTTP (Cloud Run / Container compatible)
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=port,
        )
    )