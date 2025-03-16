import matplotlib.pyplot as plt
import io
import base64

def visualisation(graphTitle, xHeader, yHeader, xData, yData):
    plt.bar(xData, yData)
    plt.xlabel(xHeader)
    plt.ylabel(yHeader)
    plt.title(graphTitle)
    print("Saving visualisation to ./visualisations/" + graphTitle + ".png")
    plt.savefig("./visualisations/" + graphTitle + ".png")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()

    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")