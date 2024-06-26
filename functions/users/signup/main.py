import json
import os
from dataclasses import dataclass

import boto3


@dataclass
class Input:
    email: str
    password: int


@dataclass
class Output:
    pass


def encrypt_with_kms(plaintext: str, kms_key_id: str) -> str:
    kms_client = boto3.client("kms")
    response = kms_client.encrypt(KeyId=kms_key_id, Plaintext=plaintext.encode())
    return response["CiphertextBlob"]


def lambda_handler(event, context):
    # Retrieve the DynamoDB table name and KMS key ID from environment variables.
    USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME", "Dev-Users")
    KMS_KEY_ID = os.environ.get("KMS_KEY_ID", "bb085039-a653-4b38-abad-b6dd4ce11ea4")

    # Initialize a DynamoDB resource.
    dynamodb = boto3.resource("dynamodb")

    # Reference the DynamoDB table.
    users_table = dynamodb.Table(USERS_TABLE_NAME)

    # Parse the request body to get user data.
    body = json.loads(event["body"])

    # Verify if the user already exists.
    user = users_table.get_item(Key={"PK": body["email"]})
    if user.get("Item"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "User already exists"}),
        }

    # Encrypt the password using KMS.
    encrypted_password = encrypt_with_kms(body["password"], KMS_KEY_ID)

    # Insert the new user into the DynamoDB table.
    users_table.put_item(Item={"PK": body["email"], "password": encrypted_password})

    # Return a successful response with the newly created user ID.
    return {"statusCode": 201}
