from infra.services import Services

class MakeGuessConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="MakeGuess",
            path="./functions/guess_the_number",
            description="Verify if the number is correct, lower or higher",
            directory="make_guess",
            environment={"GUESS_THE_NUMBER_TABLE": services.dynamo_db.guess_the_number_table.table_name},
        )

        services.api_gateway.create_endpoint("GET", "/game/{game_id}", function, public=True)

        services.dynamo_db.guess_the_number_table.grant_read_data(function)
