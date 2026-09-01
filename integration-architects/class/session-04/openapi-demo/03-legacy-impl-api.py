"""Legacy API for reverse-specification demonstration."""
from fastapi import FastAPI, HTTPException

app = FastAPI()

ORDERS = {
    "ORD-1001": {"customer_name": "ABC Retail", "status": "SHIPPED",
                 "destination": "Pune", "expected_delivery": "2026-08-25"},
    "ORD-1002": {"customer_name": "XYZ Industries", "status": "PROCESSING",
                 "destination": "Mumbai", "expected_delivery": "2026-08-28"},
}

@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    if not order_id.startswith("ORD-"):
        raise HTTPException(status_code=400, detail="Invalid order ID")
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, **order}

@app.get("/health")
def health():
    return {"status": "UP"}

# COPILOT PROMPT:
# Analyze this legacy API and generate an OpenAPI 3.1 specification describing
# CURRENT behavior. Do not redesign it. Flag anything that cannot be inferred.
