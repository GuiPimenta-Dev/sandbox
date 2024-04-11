from infra.services import Services

class DisconnectConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Disconnect",
            path="./functions/chat",
            description="real time chat",
            directory="disconnect",
            environment={"CONNECTIONS_TABLE_NAME": services.dynamo_db.connections_table.table_name}
        )

        services.websockets.create_route("$disconnect", function)

        services.dynamo_db.connections_table.grant_read_data(function)