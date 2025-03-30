from flask import Flask, jsonify, request, Response
import awsgi
import population_visualisation as pop_vis
import json

app = Flask(__name__)

def split_data(data):
    if data:
        return data.split(',')
    else:
        return []

@app.route("/")
def home():
    return jsonify(message="Hello from Flask on AWS Lambda!")

@app.route("/population/visualisation/v1", methods=['GET'])
def visualisation():
    graphTitle = request.args.get('graphTitle')
    xHeader = request.args.get('x-header')
    yHeader = request.args.get('y-header')
    xData = split_data(request.args.get('x-data'))
    yData = split_data(request.args.get('y-data'))
    try:
        yData = [float(item) for item in yData]
    except:
        return Response("y-data must be a list of numbers", status=400)
    
    try:
        image_base64 = pop_vis.bar_chart_visualisation(graphTitle, xHeader, yHeader, xData, yData)
    except ValueError as e:
        return Response(str(e), status=400)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=500)
    
    return {
        "statusCode": 200,
        "body": json.dumps({"image": image_base64}),
        "headers": {"Content-Type": "application/json"}
    }

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