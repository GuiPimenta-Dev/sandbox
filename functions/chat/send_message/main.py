import json
import os

import boto3


def lambda_handler(event, context):
    print(event)

    sender_id = event["requestContext"]["connectionId"]

    # Use the actual table name
    dynamodb = boto3.resource("dynamodb")

    CONNECTIONS_TABLE_NAME = os.environ.get("CONNECTIONS_TABLE_NAME")
    connections_table = dynamodb.Table(CONNECTIONS_TABLE_NAME)

    connections = connections_table.scan()["Items"]

    POST_TO_CONNECTION_URL = os.environ.get("POST_TO_CONNECTION_URL")

    apig_management = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=POST_TO_CONNECTION_URL,
    )
    for connection in connections:
        connection_id = connection["PK"]
        if connection_id != sender_id:
            try:
                apig_management.post_to_connection(
                    ConnectionId=connection_id,
                    Data=json.dumps({"message": json.loads(event["body"])["message"], "senderId": sender_id}),
                )
            except Exception as e:
                print(f"Error: {e}")

    return {"statusCode": 200}
