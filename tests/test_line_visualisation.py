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
    pytest.skip("Could not import line visualisation", allow_module_level=True)


@pytest.fixture
def sample_data():
    return {
        "graphTitle": "Sample Test Data",
        "xHeader": "Year",
        "yHeader": "Population",
        "xData": ["2022", "2023", "2024", "2025", "2026"],
        "yData": [[1000, 2000, 3000, 4000, 5000], [1500, 2500, 3500, 4500, 5500]],
        "labels": ["Suburb A", "Suburb B"],
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
        labels=["Suburb C", "Suburb D"],
        xData=["2050", "2060", "2070", "2071"],
        yData=[[1200.5, 1500.75, 1800.0, 2100.25], [1300.5, 1600.75, 1900.0, 2200.25]],
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_visualisation_single_data_point():
    """Test with a single data point."""
    result = multi_line_chart_visualisation(
        "Single Point", "Year", "Population", ["Suburb E"], ["2022"], [[1000.0]]
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_visualisation_empty_data():
    """Test with empty data."""
    with pytest.raises(ValueError):
        multi_line_chart_visualisation("Empty Data", "Year", "Population", [], [], [])

def test_visualisation_different_data_produces_different_images():
    """Test that different data produces different base64 outputs."""
    result1 = multi_line_chart_visualisation(
        "Sample Test Data",
        "Year",
        "Population",
        ["Suburb A", "Suburb B"],
        ["2022", "2023", "2024", "2025", "2026"],
        [[1000, 2000, 3000, 4000, 5000], [1500, 2500, 3500, 4500, 5500]],
    )
    result2 = multi_line_chart_visualisation(
        "Sample Test Data",
        "Year",
        "Population",
        ["Suburb C", "Suburb D"],
        ["2027", "2028", "2029", "2030", "2031"],
        [[1100, 2100, 3100, 4100, 5100], [1600, 2600, 3600, 4600, 5600]],
    )
    assert result1 != result2

def test_visualisation_invalid_xData():
    """Test with invalid data."""
    with pytest.raises(ValueError):
        multi_line_chart_visualisation(
            "Invalid Data",
            "Year",
            "Population",
            ["Suburb F", "Suburb G"],
            [2002],
            [[1000.0], [2000.0]],
        )

def test_visualisation_invalid_yData():
    with pytest.raises(ValueError):
        multi_line_chart_visualisation(
            "Invalid Data",
            "Year",
            "Population",
            ["Suburb H", "Suburb I"],
            ["2022", "2023"],
            [[1000.0, 2000.0], [3000.0]],
        )
    with pytest.raises(ValueError):
        multi_line_chart_visualisation(
            "Invalid Data",
            "Year",
            "Population",
            ["Suburb J", "Suburb K"],
            ["2022", "2023"],
            [[100,200], ["1000","2000"]],
        )

def test_visualisation_too_many_yData():
    """Test with too many yData."""
    with pytest.raises(ValueError):
        multi_line_chart_visualisation(
            "Too Many yData",
            "Year",
            "Population",
            ["Suburb L", "Suburb M", "Suburb N", "Suburb O"],
            ["2022", "2023"],
            [[1000.0, 2000.0], [3000.0, 4000.0], [5000.0, 6000.0], [7000.0, 8000.0]],
        )

def test_visualisation_invalid_labels():
    """Test with invalid labels."""
    with pytest.raises(ValueError):
        multi_line_chart_visualisation(
            "Invalid Labels",
            "Year",
            "Population",
            [],
            ["2022", "2023"],
            [[1000.0, 2000.0]],
        )
