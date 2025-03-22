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
    xData = request.args.get('x-data').split(',')
    yData = request.args.get('y-data').split(',')
    try:
        yData = [float(item) for item in yData]
        image_base64 = pop_vis.visualisation(graphTitle, xHeader, yHeader, xData, yData)
        return {
            "statusCode": 200,
            "body": json.dumps({"image": image_base64}),
            "headers": {"Content-Type": "application/json"}
        }
    except:
        return Response("y-data must be a list of numbers", status=400)

# Function to pass lambda request to Flask app
def lambda_handler(event, context):
    if 'httpMethod' not in event:
        if 'requestContext' in event and 'http' in event['requestContext']:
            # Convert API Gateway v2 format to the format awsgi expects
            return awsgi.response(app, convert_v2_to_v1(event), context, base64_content_types={"image/png"})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'This endpoint should be accessed through API Gateway'})
        }
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

def convert_v2_to_v1(event):
    v1_event = {
        'httpMethod': event['requestContext']['http']['method'],
        'path': event['requestContext']['http']['path'],
        'headers': event['headers'],
        'queryStringParameters': event.get('queryStringParameters', {}),
        'body': event.get('body', ''),
        'isBase64Encoded': event.get('isBase64Encoded', False)
    }
    return v1_event

if __name__ == "__main__":
    app.run()