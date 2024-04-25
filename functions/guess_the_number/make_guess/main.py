import json
from dataclasses import dataclass
import boto3
import os

@dataclass
class Path:
    game_id: str


@dataclass
class Input:
    guess: int


@dataclass
class Output:
    answer: str


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")
    GUESS_THE_NUMBER_TABLE = os.environ.get("GUESS_THE_NUMBER_TABLE")
    table = dynamodb.Table(GUESS_THE_NUMBER_TABLE)

    game_id = event["pathParameters"]["game_id"]
    guess = event["queryStringParameters"]["guess"]

    response = table.get_item(Key={"PK": game_id})
    random_number = int(response["Item"]["number"])
    
    if int(guess) == random_number:
        answer = "correct"
    elif int(guess) < random_number:
        answer = "higher"
    else:
        answer = "lower"
    

    return {"statusCode": 200, "body": json.dumps({"answer": answer})}
