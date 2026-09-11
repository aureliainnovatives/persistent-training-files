"""Tiny inventory module for the Copilot custom-agent lab."""
import json
from pathlib import Path
from typing import Any

def load_products(file_path: str | Path) -> list[dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def find_product(products: list[dict[str, Any]], sku: str) -> dict[str, Any] | None:
    for product in products:
        if product["sku"] == sku:
            return product
    return None

def total_inventory_value(products: list[dict[str, Any]]) -> float:
    return sum(p["price"] * p["quantity"] for p in products)

# The low-stock requirement is deliberately NOT implemented.
