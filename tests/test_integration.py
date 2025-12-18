import io
import json
import pytest

from app import app


# ---------------------------
# Pytest Fixture: Flask client
# ---------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------
# Integration Test 1
# Text Input Reviews
# ---------------------------
def test_analyze_with_text_input(client):
    data = {
        "product_name": "Test Phone",
        "reviews": "Good battery\nExcellent camera\nPoor speaker"
    }

    response = client.post(
        "/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    result = response.get_json()
    assert result["success"] is True
    assert result["product_name"] == "test phone"


# ---------------------------
# Integration Test 2
# CSV Upload Reviews
# ---------------------------
def test_analyze_with_csv_upload(client):
    csv_content = """review
Great product
Bad build quality
Average performance
"""

    data = {
        "product_name": "CSV Product",
        "csv_file": (io.BytesIO(csv_content.encode("utf-8")), "reviews.csv")
    }

    response = client.post(
        "/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    result = response.get_json()
    assert result["success"] is True
    assert result["product_name"] == "csv product"


# ---------------------------
# Integration Test 3
# Missing Input Validation
# ---------------------------
def test_analyze_without_reviews(client):
    data = {
        "product_name": "Invalid Product"
    }

    response = client.post(
        "/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result


# ---------------------------
# Integration Test 4
# Dashboard Page Loads
# ---------------------------
def test_dashboard_page(client):
    # First analyze a product
    data = {
        "product_name": "Dashboard Product",
        "reviews": "Nice design\nVery useful"
    }

    client.post("/analyze", data=data, content_type="multipart/form-data")

    # Now load dashboard
    response = client.get("/dashboard/dashboard product")

    assert response.status_code == 200
    assert b"Dashboard Product" in response.data
