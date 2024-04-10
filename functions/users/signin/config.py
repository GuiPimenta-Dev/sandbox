from infra.services import Services

class SigninConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Signin",
            path="./functions/users",
            description="Signin function",
            directory="signin"
        )

        services.api_gateway.create_endpoint("POST", "/users", function, public=True)

            