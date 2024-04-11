from infra.services import Services

class BroadcastConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Broadcast",
            path="./functions/chat",
            description="real time chat",
            directory="broadcast"
        )
