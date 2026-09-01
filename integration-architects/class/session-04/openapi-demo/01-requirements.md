# Order Tracking API — Requirements

## Scenario
A customer-service team needs an API to retrieve order and delivery information from a legacy order platform.

## Requirements
- `GET /api/orders/{order_id}`
- Return order ID, customer, status, destination and expected delivery.
- Valid Order ID: `ORD-` + four digits.
- Invalid ID → 400; unknown order → 404; backend unavailable → 503.
- Do not expose backend-specific fields or internal exceptions.

## Copilot Exercise
> Read this file and generate an OpenAPI 3.1 specification with schemas, validation, examples, and 400/404/503 responses. Do not invent additional functionality.

## Teaching Point
AI accelerates specification generation; the Integration Architect validates the contract.
