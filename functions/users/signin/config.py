from infra.services import Services


class SigninConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Signin",
            path="./functions/users",
            description="Signin function",
            directory="signin",
            layers=[services.layers.sm_utils_layer, services.layers.jwt_layer],
            environment={
                "USERS_TABLE_NAME": services.dynamo_db.users_table.table_name,
                "KMS_KEY_ID": services.kms.signup_key.key_id,
                "JWT_SECRET": services.secrets_manager.jwt_secret.secret_name,
            }
        )

        services.api_gateway.create_endpoint("POST", "/users", function, public=True)

        services.dynamo_db.users_table.grant_read_data(function)

        services.kms.signup_key.grant_decrypt(function)