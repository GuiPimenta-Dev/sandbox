import json
import os
import boto3

def lambda_handler(event, context):
    # Retrieve the URL for posting messages to connected clients from the environment variables
    POST_TO_CONNECTION_URL = os.environ.get("POST_TO_CONNECTION_URL")
    
    # Create a client for the API Gateway Management API, specifying the endpoint URL
    # This client is used to post messages to the connections maintained by API Gateway
    apigtw_management = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=POST_TO_CONNECTION_URL,
    )

    # Parse the incoming message and the recipient ID from the Lambda event body
    message = json.loads(event["body"])["message"]
    sender_id = event["requestContext"]["connectionId"] 
    recipient_id = json.loads(event["body"])["recipient_id"]
    
    # Iterate over both the sender and recipient connection IDs
    for connection_id in [sender_id, recipient_id]:
        # For each connection ID, post the message along with the sender and recipient IDs
        # This enables both the sender and recipient to receive the message
        apigtw_management.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({"message": message, "sender_id": sender_id, "recipient_id": recipient_id}),
        )
    
    # After successfully posting the message to both connections, return a 200 status code
    return {"statusCode": 200}
