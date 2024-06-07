from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

test_data = {
    "no_of_dependents": 4,
    "education": 1,
    "self_employed": 1,
    "income_annum": 8900000,
    "loan_amount": 34000000,
    "loan_term": 20,
    "cibil_score": 415,
    "residential_assets_value": 13500000,
    "commercial_assets_value": 3100000,
    "luxury_assets_value": 33600000,
    "bank_asset_value": 12800000,
}


test_data_bad = {
    "no_of_dependents": 4,
    "education": 1,
    "self_employed": 1,
    "income_annum": 8900000,
    "loan_amount": 34000000,
    "loan_term": 20,
    "cibil_score": 415,
    "residential_assets_value": 13500000,
    "commercial_assets_value": 3100000,
    "luxury_assets_value": 33600000,
    "bank_asset_value": "string",
}


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["still"] == "alive"


def test_api_response():
    response = client.post(
        "/api/V1/predict",
        json=test_data,
    )
    assert response.status_code == 200
    assert response.json()["loan_approval_status"] == "Rejected"


def test_api_response_bad_data():
    response = client.post(
        "/api/V1/predict",
        json=test_data_bad,
    )
    assert response.status_code == 422
    assert response.json()["data"] == "Invalid input"
    assert response.json()["success"] == False


def test_api_response_404():
    response = client.post(
        "/api/V1/predict/model",
        json=test_data_bad,
    )
    assert response.status_code == 404
    assert response.json()["data"] == "Not Found"
    assert response.json()["success"] == False
