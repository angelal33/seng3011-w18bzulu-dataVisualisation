import matplotlib.pyplot as plt
import io
import base64


def check_bar_chart_data(xData, yData):
    if (
        xData in [[], None]
        or yData in [[], None]
        or not isinstance(xData, list)
        or not isinstance(yData, list)
    ):
        return ValueError("xData and yData must not be empty")
    elif len(xData) != len(yData):
        return ValueError("xData and yData must have the same length")
    elif not all(isinstance(item, str) for item in xData):
        return ValueError("xData must be a list of strings")
    elif not all(isinstance(item, (int, float)) for item in yData):
        return ValueError("yData must be a list of numbers")
    return None


def bar_chart_visualisation(graphTitle, xHeader, yHeader, xData, yData):
    error = check_bar_chart_data(xData, yData)
    if error:
        raise error
    plt.bar(xData, yData)
    plt.xlabel(xHeader)
    plt.ylabel(yHeader)
    plt.title(graphTitle)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()

    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def check_line_chart_data(labels, xData, yData):
    if len(labels) != len(yData):
        raise ValueError("labels and yData must have the same length")
    elif len(labels) == 0 or len(xData) == 0 or len(yData) == 0:
        raise ValueError(
            f"{'labels, ' if len(labels) == 0 else ''}{'xData, ' if len(xData) == 0 else ''}"
            + f"{'yData, ' if len(yData) == 0 else ''}must not be empty"
        )
    for i in range(len(yData)):
        error = check_bar_chart_data(xData, yData[i])
        if error:
            raise error
    return None


def multi_line_chart_visualisation(
    graphTitle, xHeader, yHeader, labels, xData, yData, max_y=3
):
    error = check_line_chart_data(labels, xData, yData)
    if error:
        raise error
    if not (graphTitle and xHeader and yHeader):
        raise ValueError("graphTitle, xHeader, and yHeader must not be empty")

    if len(yData) > max_y:
        raise ValueError(f"yData must not have more than {max_y} items")

    for i in range(len(labels)):
        plt.plot(xData, yData[i], label=labels[i])
    plt.xlabel(xHeader)
    plt.ylabel(yHeader)
    plt.title(graphTitle)
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()

    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
