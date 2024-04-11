from infra.services import Services


class SendMessageConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="SendMessage",
            path="./functions/chat",
            description="real time chat",
            directory="send_message",
            environment={
                "CONNECTIONS_TABLE_NAME": services.dynamo_db.connections_table.table_name,
                "POST_TO_CONNECTION_URL": services.websockets.post_to_connection_url,
            },
        )

        services.websockets.create_route("sendMessage", function)

        services.dynamo_db.connections_table.grant_read_data(function)
