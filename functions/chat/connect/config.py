from infra.services import Services
from aws_cdk import aws_iam as iam


class ConnectConfig:
    def __init__(self, services: Services, context) -> None:

        send_connection_id_function = services.aws_lambda.create_function(
            name="SendConnectionId",
            path="./functions/chat",
            description="Return the connection id on connect",
            directory="send_connection_id",
            environment={
                "POST_TO_CONNECTION_URL": context.resources["post_to_connection_url"]
            },
        )

        send_connection_id_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["execute-api:ManageConnections"],
                resources=["*"],
            )
        )

        connect_function = services.aws_lambda.create_function(
            name="Connect",
            path="./functions/chat",
            description="real time chat",
            directory="connect",
            environment={
                "CONNECTIONS_TABLE_NAME": services.dynamo_db.connections_table.table_name,
                "TARGET_FUNCTION_ARN": send_connection_id_function.function_arn 
            },
        )

        services.websockets.create_route("$connect", connect_function)

        send_connection_id_function.grant_invoke(connect_function)

        services.dynamo_db.connections_table.grant_write_data(connect_function)