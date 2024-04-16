from infra.services import Services
from aws_cdk import aws_iam as iam


class SendConnectionIdConfig:
    def __init__(self, services: Services, context) -> None:

        function = services.aws_lambda.create_function(
            name="SendConnectionId",
            path="./functions/chat",
            description="Return the connection id on connect",
            directory="send_connection_id",
            environment={"POST_TO_CONNECTION_URL": context.resources["post_to_connection_url"]},
        )

        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["execute-api:ManageConnections"],
                resources=[f"arn:aws:execute-api:*:*:*"],
            )
        )
