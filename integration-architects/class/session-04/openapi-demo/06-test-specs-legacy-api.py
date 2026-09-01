import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


IMPLEMENTATION_PATH = Path(__file__).with_name("03-legacy-api.py")
module_spec = importlib.util.spec_from_file_location("legacy_api", IMPLEMENTATION_PATH)
if module_spec is None or module_spec.loader is None:
    raise ImportError(f"Unable to load {IMPLEMENTATION_PATH}")

legacy_api = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(legacy_api)
client = TestClient(legacy_api.app)


def test_known_order_returns_legacy_payload():
    response = client.get("/api/orders/ORD-1001")

    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ORD-1001",
        "customer_name": "ABC Retail",
        "status": "SHIPPED",
        "destination": "Pune",
        "expected_delivery": "2026-08-25",
    }


def test_second_known_order_returns_legacy_payload():
    response = client.get("/api/orders/ORD-1002")

    assert response.status_code == 200
    assert response.json()["customer_name"] == "XYZ Industries"
    assert response.json()["expected_delivery"] == "2026-08-28"


def test_non_prefixed_order_id_returns_400():
    response = client.get("/api/orders/ABC-1234")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid order ID"}


def test_prefixed_but_malformed_order_id_is_treated_as_unknown():
    response = client.get("/api/orders/ORD-ABC")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_prefixed_unknown_order_returns_404():
    response = client.get("/api/orders/ORD-9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_health_endpoint_returns_up():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}
