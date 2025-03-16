from flask import Flask, jsonify, send_file, request
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
    xHeader = request.args.get('xHeader')
    yHeader = request.args.get('yHeader')
    xData = request.args.getlist('xData')
    yData = request.args.getlist('yData')
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