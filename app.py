from flask import Flask, jsonify, request, Response
import awsgi
import population_visualisation as pop_vis
import json

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello from Flask on AWS Lambda!")

@app.route("/population/visualisation/v1", methods=['GET'])
def visualisation():
    graphTitle = request.args.get('graphTitle')
    xHeader = request.args.get('x-header')
    yHeader = request.args.get('y-header')
    xData = request.args.getlist('x-data')
    try:
        yData = [float(item) for item in request.args.getlist('y-data')]
    except:
        return Response("y-data must be a list of numbers", status=400)
    print(graphTitle, xHeader, yHeader, xData, yData)
    image_base64 = pop_vis.visualisation(graphTitle, xHeader, yHeader, xData, yData)
    return {
        "statusCode": 200,
        "body": json.dumps({"image": image_base64}),
        "headers": {"Content-Type": "application/json"}
    }

def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

if __name__ == "__main__":
    app.run()