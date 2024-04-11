from infra.services import Services


class ConnectConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Connect",
            path="./functions/chat",
            description="real time chat",
            directory="connect",
            environment={
                "CONNECTIONS_TABLE_NAME": services.dynamo_db.connections_table.table_name,
            },
        )

        services.websockets.create_route("$connect", function)

        services.dynamo_db.connections_table.grant_write_data(function)
