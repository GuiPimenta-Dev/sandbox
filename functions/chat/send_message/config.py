from infra.services import Services
from aws_cdk import aws_iam as iam


class SendMessageConfig:
    def __init__(self, services: Services, context) -> None:

        function = services.aws_lambda.create_function(
            name="SendMessage",
            path="./functions/chat",
            description="real time chat",
            directory="send_message",
            environment={
                "POST_TO_CONNECTION_URL": context.resources["post_to_connection_url"],
            },
        )

        services.websockets.create_route("sendMessage", function)

        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["execute-api:ManageConnections"],
                resources=[f"arn:aws:execute-api:*:*:*"],
            )
        )
