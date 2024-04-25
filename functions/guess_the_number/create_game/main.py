import json
from dataclasses import dataclass
import random
import uuid
import boto3
import os


@dataclass
class Input:
    pass


@dataclass
class Output:
    message: str


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")
    GUESS_THE_NUMBER_TABLE = os.environ.get("GUESS_THE_NUMBER_TABLE")
    table = dynamodb.Table(GUESS_THE_NUMBER_TABLE)

    body = json.loads(event["body"])
    initial_number = body.get("initial_number", 1)
    end_number = body.get("end_number", 100)

    if initial_number >= end_number:
        return {"statusCode": 400, "body": json.dumps({"message": "initial_number must be less than end_number"})}

    game_id = str(uuid.uuid4())
    random_number = random.randint(initial_number, end_number)

    table.put_item(
        Item={
            "PK": game_id,
            "number": random_number,
        }
    )

    return {"statusCode": 200, "body": json.dumps({"game_id": game_id})}
