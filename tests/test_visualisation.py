import base64
import sys
import os
import pytest

# Add the parent directory to sys.path so we can import visualisation.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

try:
    from population_visualisation import bar_chart_visualisation
except ImportError:
    pytest.skip("Could not import visualisation", allow_module_level=True)


@pytest.fixture
def sample_data():
    return {
        "graphTitle": "Sample Test Data",
        "xHeader": "Year",
        "yHeader": "Population",
        "xData": ["2022", "2023", "2024", "2025", "2026"],
        "yData": [1000, 2000, 3000, 4000, 5000],
    }


def test_visualisation_output_type(sample_data):
    """Test that the output is a base64-encoded string."""
    result = bar_chart_visualisation(**sample_data)
    assert isinstance(result, str)

    try:
        base64.b64decode(result)
    except Exception:
        pytest.fail("Result is not valid base64-encoded data.")


def test_visualisation_output_not_empty(sample_data):
    """Test that the output is not an empty string."""
    result = bar_chart_visualisation(**sample_data)
    assert len(result) > 0, "Base64 encoded image should not be empty"


def test_visualisation_different_data():
    """Test with different data to ensure variety works."""
    result = bar_chart_visualisation(
        "Sample Test Data",
        "Year",
        "Population",
        ["2050", "2060", "2070", "2071"],
        [1200.5, 1500.75, 1800.0, 2100.25],
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_visualisation_single_data_point():
    """Test with a single data point."""
    result = bar_chart_visualisation(
        "Single Point", "Year", "Population", ["2022"], [1000.0]
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_visualisation_different_data_produces_different_images():
    """Test that different data produces different base64 outputs."""
    result1 = bar_chart_visualisation(
        "Quarterly Sales",
        "Quarter",
        "Revenue",
        ["Q1", "Q2", "Q3", "Q4"],
        [1200.5, 1500.75, 1800.0, 2100.25],
    )
    result2 = bar_chart_visualisation(
        "Population Data",
        "Year",
        "Population",
        ["2000", "2001", "2002", "2003"],
        [1000.0, 2000.0, 3000.0, 4000.0],
    )
    assert result1 != result2


# CAN BE ADDED IN WHEN ERROR CHECKING IS ADDED TO VISUALISATION.


def test_visualisation_empty_data(sample_data):
    """Test with empty data."""
    with pytest.raises(ValueError, match="xData and yData must not be empty"):
        bar_chart_visualisation(
            sample_data["graphTitle"],
            sample_data["xHeader"],
            sample_data["yHeader"],
            [],
            [],
        )
    with pytest.raises(ValueError, match="graphTitle must not be empty"):
        bar_chart_visualisation(
            "",
            "",
            "",
            [],
            [],
        )


def test_visualisation_bad_data(sample_data):
    """Test with bad data."""
    with pytest.raises(ValueError, match="xData must be a list of strings"):
        bar_chart_visualisation(
            sample_data["graphTitle"],
            sample_data["xHeader"],
            sample_data["yHeader"],
            [2022, 2023, 2024, 2025, 2026],
            sample_data["yData"],
        )
    with pytest.raises(ValueError, match="yData must be a list of numbers"):
        bar_chart_visualisation(
            sample_data["graphTitle"],
            sample_data["xHeader"],
            sample_data["yHeader"],
            sample_data["xData"],
            ["a", "b", "c", "d", "e"],
        )


def test_visualisation_mismatched_data_lengths():
    """Test with mismatched x and y data lengths."""
    with pytest.raises(ValueError, match="xData and yData must have the same length"):
        bar_chart_visualisation("Mismatched Data", "X", "Y", ["2022", "2023"], [1000.0])


def test_visualisation_handles_non_numeric_ydata(sample_data):
    """Test that non-numeric y-data raises an exception."""
    with pytest.raises(ValueError, match="yData must be a list of numbers"):
        bar_chart_visualisation(
            sample_data["graphTitle"],
            sample_data["xHeader"],
            sample_data["yHeader"],
            sample_data["xData"],
            ["a", "b", "c", "d", "e"],
        )
