import os

import boto3


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")

    CONNECTIONS_TABLE_NAME = os.environ.get("CONNECTIONS_TABLE_NAME")
    connections_table = dynamodb.Table(CONNECTIONS_TABLE_NAME)

    connection_id = event["requestContext"]["connectionId"]
    connections_table.delete_item(Key={"PK": connection_id})

    return {"statusCode": 200}
