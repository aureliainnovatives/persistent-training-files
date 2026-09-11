# Inventory Mini-App — Requirements

## Existing behavior
Products contain `sku`, `name`, `price`, and `quantity`. The application already loads JSON, finds products by SKU, and calculates inventory value.

## New Requirement — Low-Stock Report
1. Low stock means **`quantity < threshold`**.
2. Threshold is configurable; default is `10`.
3. Quantity exactly equal to threshold is NOT low stock.
4. Sort results from lowest to highest quantity.
5. Each result contains SKU, name, and current quantity.
6. No matches returns an empty list.
7. Negative threshold raises `ValueError`.

## Acceptance tests
Cover default threshold, custom threshold, exact boundary, sorting, empty result, and negative threshold.
