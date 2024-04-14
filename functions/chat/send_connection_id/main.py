import json
import os
import boto3

def lambda_handler(event, context):
    connection_id = event["connection_id"]

    api_gateway_management_client = boto3.client("apigatewaymanagementapi", endpoint_url=os.get("POST_TO_CONNECTION_URL"))

    # Send the payload to the WebSocket
    api_gateway_management_client.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps({"sender_id": connection_id}).encode("utf-8")
    )

    return {"statusCode": 200}
