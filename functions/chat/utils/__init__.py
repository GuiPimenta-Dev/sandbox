import json
import boto3


def invoke_lambda(connection_id, function_arn):
    lambda_client = boto3.client("lambda")

    # Specify the ARN of the second Lambda function

    # Define the payload to pass to the second Lambda function
    payload = {"connection_id": connection_id}

    # Invoke the second Lambda function asynchronously
    lambda_client.invoke(FunctionName=function_arn, InvocationType="Event", Payload=json.dumps(payload))
