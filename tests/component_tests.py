# from moto import mock_aws
# from moto import mock_lambda
# from moto.awslambda.models import LambdaModel
# from moto.awslambda.exceptions import LambdaException
import pytest
import requests
import json

# # @mock_aws(config={"lambda": {"use_docker": False}})

# mock_lambda = mock_lambda()
# @mock_lambda
# def test_lambda_function():
#     """Test the Lambda function."""
#     # Mock the Lambda function
#     lambda_client = LambdaModel()
#     lambda_client.create_function(
#         FunctionName="test_lambda_function",
#         Runtime="python3.8",
#         Role="role",
#         Handler="app.lambda_handler",
#         Code={
#             "ZipFile": b"def lambda_handler(event, context): return {'statusCode': 200, 'body': 'Hello from Lambda!'}"
#         },
#     )

#     # Invoke the Lambda function
#     response = lambda_client.invoke(FunctionName="test_lambda_function")
#     assert response["StatusCode"] == 200
#     assert response["Payload"].read() == b"Hello from Lambda!"


def test_single_suburb():
    resp = requests.get(
      "https://f8jc59emd2.execute-api.us-east-1.amazonaws.com/dev/population/visualisation/v1",
      params={
        "graphTitle": "Sample Test Data",
        "x-header": "Year",
        "y-header": "Population",
        "x-data": ','.join(["2022", "2023", "2024", "2025", "2026"]),
        "y-data": ','.join(str(x) for x in [1000, 2000, 3000, 4000, 5000])
      }
    )
    assert resp.status_code == 200
    result = json.loads(resp.json()['body'])
    assert "image" in result
    assert isinstance(result["image"], str)
    assert len(result["image"]) > 0, "Base64 encoded image should not be empty"

def test_multiple_suburb():
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

    resp = requests.get(
      "https://f8jc59emd2.execute-api.us-east-1.amazonaws.com/dev/populations/visualisation/v1",
      params=data
    )
    assert resp.status_code == 200
    result = json.loads(resp.json()['body'])
    assert "image" in result
    assert isinstance(result["image"], str)
    assert len(result["image"]) > 0, "Base64 encoded image should not be empty"