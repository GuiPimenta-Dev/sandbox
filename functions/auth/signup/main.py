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
    USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME")
    KMS_KEY_ID = os.environ.get("KMS_KEY_ID")

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

    # WAITING: something really long
    # Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum mattis porttitor ex, eget consectetur dolor maximus eu. Sed blandit malesuada leo in varius. Maecenas ornare felis magna, id rhoncus elit efficitur non. Fusce vitae posuere sapien, nec pulvinar risus. Duis consequat hendrerit consequat. Pellentesque nec porttitor lorem. Fusce sed mauris quis elit tincidunt placerat. Duis quis pharetra turpis, et convallis lacus. Mauris sed est sapien. Nam accumsan lacus mi, in pellentesque mauris malesuada vitae.
    #
    # Vestibulum sit amet massa ac velit condimentum dignissim. In hendrerit, ligula aliquet luctus dignissim, ex mauris pulvinar enim, quis luctus massa eros in nisi. Sed tempor ante et ligula porta, vitae faucibus ipsum consectetur. Vivamus nec dictum neque, finibus vulputate eros. In hac habitasse platea dictumst. Vivamus commodo est mi, quis varius dolor egestas sit amet. Nullam dui dui, posuere vitae nisl sed, dictum maximus felis. Maecenas luctus ultricies elementum. Quisque quis nibh venenatis, malesuada diam et, consequat nibh. Proin suscipit tristique rhoncus. Nam faucibus, sem eu pharetra sodales, ex erat efficitur odio, ut viverra enim mi vitae velit.
    #
    # Pellentesque sodales dui sit amet ante blandit posuere. Phasellus enim risus, vulputate blandit augue vitae, luctus dapibus libero. Aenean malesuada ante sed consequat aliquet. Curabitur volutpat fringilla erat nec accumsan. Vestibulum eu ligula tortor. Mauris vitae placerat leo. Nam vulputate et ante et ultricies. Maecenas cursus maximus venenatis. Aliquam est mauris, bibendum eu aliquet sit amet, sagittis et sapien. Mauris elit justo, ornare a euismod ut, euismod sed odio. Phasellus dignissim magna non neque aliquam, non ornare turpis facilisis. Etiam vitae ex tincidunt, scelerisque nibh vel, viverra dolor. Duis eu tincidunt quam. Donec elementum lorem est, sed vestibulum odio lobortis tincidunt. Suspendisse suscipit tellus leo. Nulla dictum massa et magna suscipit dignissim.
    #
    # Sed id molestie nisl. Nunc semper tellus eu turpis tempor, ut tincidunt leo porta. In quis imperdiet justo, sit amet suscipit arcu. Morbi lobortis luctus nulla in iaculis. Aenean quis libero venenatis, gravida erat sit amet, rutrum urna. Nulla vitae congue ligula, nec ultricies lectus. Aliquam at nisi vitae nunc porttitor consequat at eu dolor. Phasellus ullamcorper varius sapien non consectetur. Nullam molestie suscipit velit at consectetur. In consectetur orci quis pretium convallis. Integer eget ornare lorem.
    #
    # Nullam dictum scelerisque pellentesque. Etiam quis ex nunc. Donec imperdiet, mi sit amet placerat venenatis, nibh ante semper mi, sagittis hendrerit lectus felis non nisl. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut a iaculis ex, ullamcorper tincidunt eros. Aliquam vitae nisi dolor. Vestibulum pulvinar nisl enim, vel dictum enim fringilla quis. Nunc at magna pellentesque, rutrum lacus eget, malesuada nisi. Pellentesque lobortis leo non malesuada cursus. Etiam eleifend viverra magna, ut eleifend nunc accumsan id. Aenean fringilla ut ipsum vitae tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

    # HELP: something really long
    # that i am not aware of
    # i need to do

    # IMPROVE: something really long
    # that i am not aware of
    # i need to do

    # Encrypt the password using KMS.
    encrypted_password = encrypt_with_kms(body["password"], KMS_KEY_ID)

    # Insert the new user into the DynamoDB table.
    users_table.put_item(Item={"PK": body["email"], "password": encrypted_password})

    # Return a successful response with the newly created user ID.
    return {"statusCode": 201}
