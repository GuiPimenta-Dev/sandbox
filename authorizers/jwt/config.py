from infra.services import Services


class JwtAuthorizerConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="JwtAuthorizer",
            path="./authorizers/jwt",
            layers=[services.layers.jwt_layer],
            description="An authorizer for private lambda functions",
        )

        services.api_gateway.create_authorizer(function, name="jwt", default=True)
