import json
import os

import boto3


def invoke_second_lambda(connection_id):
    lambda_client = boto3.client("lambda")

    TARGET_FUNCTION_ARN = os.environ.get("TARGET_FUNCTION_ARN")

    # Define the payload to pass to the second Lambda function
    payload = {"connection_id": connection_id}

    # Invoke the second Lambda function asynchronously
    lambda_client.invoke(FunctionName=TARGET_FUNCTION_ARN, InvocationType="Event", Payload=json.dumps(payload))


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")

    CONNECTIONS_TABLE_NAME = os.environ.get("CONNECTIONS_TABLE_NAME")
    connections_table = dynamodb.Table(CONNECTIONS_TABLE_NAME)

    connection_id = event["requestContext"]["connectionId"]
    connections_table.put_item(Item={"PK": connection_id})

    invoke_second_lambda(connection_id)

    return {"statusCode": 200}
