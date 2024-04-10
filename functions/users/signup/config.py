from infra.services import Services


class SignUpConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="CreateUser",
            path="./functions/users",
            description="Create a user with name and age on Dynamo DB",
            directory="signup",
            environment={
                "USERS_TABLE_NAME": services.dynamo_db.users_table.table_name,
                "KMS_KEY_ID": services.kms.signup_key.key_id,
            },
        )

        services.api_gateway.create_endpoint("POST", "/signup", function, public=True)

        services.dynamo_db.users_table.grant_read_write_data(function)

        services.kms.signup_key.grant_encrypt(function)
