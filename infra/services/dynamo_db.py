from aws_cdk import aws_dynamodb as dynamo_db
from aws_cdk import aws_iam as iam


class DynamoDB:
    def __init__(self, scope, context) -> None:

        self.guess_the_number_table = dynamo_db.Table.from_table_arn(
            scope,
            "GuessTheNumberTable",
            "arn:aws:dynamodb:us-east-2:211125768252:table/Dev-Guess-The-Number",
        )

        self.users_table = dynamo_db.Table.from_table_arn(
            scope,
            "UsersTable",
            "arn:aws:dynamodb:us-east-2:211125768252:table/Dev-Users",
        )

        self.connections_table = dynamo_db.Table.from_table_arn(
            scope,
            "ConnectionsTable",
            "arn:aws:dynamodb:us-east-2:211125768252:table/Connections",
        )

    @staticmethod
    def add_query_permission(table, function):
        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:Query"],
                resources=[f"{table.table_arn}/index/*"],
            )
        )
