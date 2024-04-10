import json
from dataclasses import dataclass


@dataclass
class Input:
    pass


@dataclass
class Output:
    message: str


def lambda_handler(event, context):

    email = event["requestContext"]["authorizer"]["email"]

    # Your function logic here
    if email:
        # Process the request with user_email
        return {"statusCode": 200, "body": json.dumps({"message": f"Hello, {email}!"})}
    else:
        # Handle the case where user_email is not available
        return {"statusCode": 401, "body": "Unauthorized"}
