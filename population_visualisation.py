import matplotlib
import matplotlib.pyplot as plt
import io
import base64

# otherData is [graphTitle, xHeader, yHeader]
def check_bar_chart_data(xData, yData, otherData={}):
    for item in otherData.keys():
        if not otherData[item]:
            return ValueError(f"{item} must not be empty")
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
    error = check_bar_chart_data(xData, yData, {graphTitle, xHeader, yHeader})
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