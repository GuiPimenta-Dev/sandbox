from infra.services import Services


class CreateGameConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="CreateGame",
            path="./functions/guess_the_number",
            description="Creates a new guess the number game",
            directory="create_game",
            environment={"GUESS_THE_NUMBER_TABLE": services.dynamo_db.guess_the_number_table.table_name},
        )

        services.api_gateway.create_endpoint("POST", "/game", function, public=True)
        
        services.dynamo_db.guess_the_number_table.grant_write_data(function)
