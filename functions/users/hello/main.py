import json
from dataclasses import dataclass


@dataclass
class Input:
    pass


@dataclass
class Output:
    message: str


def lambda_handler(event, context):

    user_email = context.get("email")

    # Your function logic here
    if user_email:
        # Process the request with user_email
        return {"statusCode": 200, "body": f"Hello, {user_email}!"}
    else:
        # Handle the case where user_email is not available
        return {"statusCode": 401, "body": "Unauthorized"}
