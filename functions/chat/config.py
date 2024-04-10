from infra.services import Services


class ChatConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="testchat",
            path="./functions/chat",
            description="real time chat",
        )

        services.websockets.create_route("$connect", function)
        services.websockets.create_route("$disconnect", function)
        services.websockets.create_route("sendmessage", function)


        services.dynamo_db.connections_table.grant_read_write_data(function)
