import pytest
import json
import os
import sys
import base64

# Add the parent directory to sys.path so we can import visualisation.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

try:
    from app import app as app_imp
except ImportError:
    pytest.skip("Could not import flask", allow_module_level=True)

@pytest.fixture()
def app():
    app = app_imp
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def sample_single():
    return {
        "graphTitle": "Sample Test Data",
        "x-header": "Year",
        "y-header": "Population",
        "x-data": ','.join(["2022", "2023", "2024", "2025", "2026"]),
        "y-data": ','.join(str(x) for x in [1000, 2000, 3000, 4000, 5000])
    }

@pytest.fixture()
def sample_multi():
    data = {
        "graphTitle": "Sample Test Data",
        "x-header": "Year",
        "y-header": "Population",
        "x-data": ["2022", "2023", "2024", "2025", "2026"],
        "y-data": [[1000, 2000, 3000, 4000, 5000], [1500, 2500, 3500, 4500, 5500]],
        "labels": ["Suburb A", "Suburb B"],
    }
    data["y-data"] = ",".join([('-').join(str(x) for x in i) for i in data["y-data"]])
    data["x-data"] = ",".join(data["x-data"])
    data["labels"] = ",".join(data["labels"])
    return data

def test_single_suburb(client, sample_single):
    resp = client.get(
      "/population/visualisation/v1",
      query_string=sample_single
    )
    assert resp.status_code == 200
    result = json.loads(resp.json['body'])
    assert "image" in result
    assert isinstance(result["image"], str)
    assert len(result["image"]) > 0, "Base64 encoded image should not be empty"
    try:
        base64.b64decode(result["image"])
    except Exception:
        pytest.fail("Result is not valid base64-encoded data.")

def test_multiple_suburb(client, sample_multi):
    resp = client.get(
      "/populations/visualisation/v1",
      query_string=sample_multi
    )
    assert resp.status_code == 200
    result = json.loads(resp.json['body'])
    assert "image" in result
    assert isinstance(result["image"], str)
    assert len(result["image"]) > 0, "Base64 encoded image should not be empty"
    try:
        base64.b64decode(result["image"])
    except Exception:
        pytest.fail("Result is not valid base64-encoded data.")
