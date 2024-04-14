import json
import os

import boto3


def lambda_handler(event, context):

    POST_TO_CONNECTION_URL = os.environ.get("POST_TO_CONNECTION_URL")
    apigtw_management = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=POST_TO_CONNECTION_URL,
    )

    recipient_id = json.loads(event["body"])["recipient_id"]
    apigtw_management.post_to_connection(
        ConnectionId=recipient_id,
        Data=json.dumps({"message": json.loads(event["body"])["message"]}),
    )

    sender_id = event["requestContext"]["connectionId"]
    apigtw_management.post_to_connection(
        ConnectionId=sender_id,
        Data=json.dumps({"message": json.loads(event["body"])["message"]}),
    )


    return {"statusCode": 200}
