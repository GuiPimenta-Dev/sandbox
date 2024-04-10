import json
from dataclasses import dataclass
import os
import jwt
import boto3


@dataclass
class Input:
    pass

@dataclass
class Output:
    message: str


def decrypt_with_kms(ciphertext_blob: bytes, kms_key_id: str) -> str:
    kms_client = boto3.client('kms')

    # Then you can pass the decoded string to the decrypt method
    response = kms_client.decrypt(
        CiphertextBlob=bytes(ciphertext_blob),
        KeyId=kms_key_id
    )
    return response['Plaintext'].decode()


def lambda_handler(event, context):
    # Retrieve the DynamoDB table name and KMS key ID from environment variables.
    USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME", "Dev-Users")
    KMS_KEY_ID = os.environ.get("KMS_KEY_ID", "bb085039-a653-4b38-abad-b6dd4ce11ea4")
    JWT_SECRET = os.environ.get("JWT_SECRET", "abc")

    # Parse the request body to get user credentials.
    body = json.loads(event["body"])
    email = body["email"]
    password = body["password"]

    # Initialize a DynamoDB resource.
    dynamodb = boto3.resource("dynamodb")
    users_table = dynamodb.Table(USERS_TABLE_NAME)

    # Retrieve user data from DynamoDB.
    response = users_table.get_item(        Key={            "PK": email        }    )
    user = response.get("Item")

    # Check if user exists.
    if not user:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "User not found"})
        }

    # Check if user exists and password matches.
    encrypted_password = user.get("password")
    decrypted_password = decrypt_with_kms(encrypted_password, KMS_KEY_ID)
    
    # Compare the decrypted password with the provided one.
    if password == decrypted_password:
        # Generate JWT token
        token = jwt.encode({"email": email}, JWT_SECRET, algorithm="HS256" )
        status_code = 200
        body = json.dumps({"token": token})
    
    else:
        status_code = 401
        body = json.dumps({"error": "Invalid credentials"})

    return { "statusCode": status_code, "body": body }        
lambda_handler({'body': '{"email": "guialvespimenta27@gmail.com", "password": "123456"}'}, None)