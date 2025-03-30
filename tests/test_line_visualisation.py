import base64
import sys
import os
import pytest

# Add the parent directory to sys.path so we can import visualisation.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

try:
    from population_visualisation import multi_line_chart_visualisation
except ImportError:
    pytest.skip("Could not import visualisation", allow_module_level=True)


@pytest.fixture
def sample_data():
    return {
        "graphTitle": "Sample Test Data",
        "xHeader": "Year",
        "yHeader": "Population",
        "xData": ["2022", "2023", "2024", "2025", "2026"],
        "yData": [[1000, 2000, 3000, 4000, 5000], [1500, 2500, 3500, 4500, 5500]],
        "labels": ["Country A", "Country B"],
    }


def test_visualisation_output_type(sample_data):
    """Test that the output is a base64-encoded string."""
    result = multi_line_chart_visualisation(**sample_data)
    assert isinstance(result, str)

    try:
        base64.b64decode(result)
    except Exception:
        pytest.fail("Result is not valid base64-encoded data.")


def test_visualisation_output_not_empty(sample_data):
    """Test that the output is not an empty string."""
    result = multi_line_chart_visualisation(**sample_data)
    assert len(result) > 0, "Base64 encoded image should not be empty"


def test_visualisation_different_data():
    """Test with different data to ensure variety works."""
    result = multi_line_chart_visualisation(
        "Sample Test Data",
        "Year",
        "Population",
        xData=["2050", "2060", "2070", "2071"],
        yData=[[1200.5, 1500.75, 1800.0, 2100.25], [1300.5, 1600.75, 1900.0, 2200.25]],
        labels=["Country C", "Country D"],
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_visualisation_single_data_point():
    """Test with a single data point."""
    result = multi_line_chart_visualisation(
        "Single Point", "Year", "Population", ["Country E"], ["2022"], [[1000.0]]
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_visualisation_empty_data():
    """Test with empty data."""
    with pytest.raises(ValueError, match="labels, xData, yData, must not be empty"):
        multi_line_chart_visualisation("Empty Data", "Year", "Population", [], [], [])


def test_visualisation_invalid_xData():
    """Test with invalid data."""
    with pytest.raises(ValueError):
        multi_line_chart_visualisation(
            "Invalid Data",
            "Year",
            "Population",
            ["Country F", "Coutry G"],
            [2002],
            [[1000.0], [2000.0]],
        )
