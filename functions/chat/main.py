import json
import boto3

# Use the actual table name
dynamodb = boto3.resource("dynamodb")
connections_table = dynamodb.Table("Connections")


def main(event, context):

    connection_id = event["requestContext"]["connectionId"]
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect":
        # Handle connection
        add_connection(connection_id)
    elif route_key == "$disconnect":
        # Handle disconnection
        delete_connection(connection_id)
    else:
        # Handle messaging
        broadcast_message(event["body"], connection_id)

    return {"statusCode": 200}


def add_connection(connection_id):
    connections_table.put_item(Item={"connectionId": connection_id})


def delete_connection(connection_id):
    connections_table.delete_item(Key={"connectionId": connection_id})


def broadcast_message(message_body, sender_id):
    connections = connections_table.scan()["Items"]
    apig_management = boto3.client(
        "apigatewaymanagementapi", endpoint_url="https://tmr3tat2fd.execute-api.us-east-2.amazonaws.com/dev"
    )
    for connection in connections:
        connection_id = connection["connectionId"]
        if connection_id != sender_id:
            try:
                apig_management.post_to_connection(
                    ConnectionId=connection_id,
                    Data=json.dumps({"message": message_body, "senderId": sender_id}),
                )
            except Exception as e:
                print(f"Error: {e}")
