from infra.services import Services


class ChatConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Chat",
            path="./functions/chat",
            description="real time chat",
        )

        services.websockets.create_websocket(name="MyWSSChat", function=function)

        services.dynamo_db.connections_table.grant_read_write_data(function)
