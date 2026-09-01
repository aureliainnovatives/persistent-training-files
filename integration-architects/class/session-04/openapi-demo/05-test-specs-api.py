import importlib.util
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


IMPLEMENTATION_PATH = Path(__file__).with_name("04-specs-api.py")
module_spec = importlib.util.spec_from_file_location("specs_api", IMPLEMENTATION_PATH)
if module_spec is None or module_spec.loader is None:
    raise ImportError(f"Unable to load {IMPLEMENTATION_PATH}")

specs_api = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(specs_api)
client = TestClient(specs_api.app)


@pytest.mark.parametrize("order_id", ["ABC-1234", "ORD-123", "ORD-12345", "ORD-ABCD", "ORD-"])
def test_invalid_order_id_returns_400(order_id):
    response = client.get(f"/api/orders/{order_id}")

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid order ID."}


def test_known_order_returns_public_contract():
    response = client.get("/api/orders/ORD-1001")

    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ORD-1001",
        "customer": "ABC Retail",
        "status": "SHIPPED",
        "destination": "Pune",
        "expected_delivery": "2026-08-25T18:00:00Z",
    }
    assert set(response.json()) == {
        "order_id",
        "customer",
        "status",
        "destination",
        "expected_delivery",
    }


def test_unknown_order_returns_404():
    response = client.get("/api/orders/ORD-9999")

    assert response.status_code == 404
    assert response.json() == {"message": "Order not found."}


def test_backend_failure_returns_sanitized_503(monkeypatch):
    class UnavailableOrders:
        def get(self, order_id):
            raise specs_api.BackendUnavailableError

    monkeypatch.setattr(specs_api, "ORDERS", UnavailableOrders())

    response = client.get("/api/orders/ORD-1001")

    assert response.status_code == 503
    assert response.json() == {
        "message": "Order service temporarily unavailable."
    }


def test_health_endpoint_is_not_exposed():
    response = client.get("/health")

    assert response.status_code == 404
