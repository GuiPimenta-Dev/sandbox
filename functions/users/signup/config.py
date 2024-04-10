from infra.services import Services


class CreateUserConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="CreateUser",
            path="./functions/users",
            description="Create a user with name and age on Dynamo DB",
            directory="create_user",
            environment={
                "USERS_TABLE_NAME": services.dynamo_db.users_table.table_name,
            },
        )

        services.api_gateway.create_endpoint("POST", "/users", function, public=True)

        services.dynamo_db.users_table.grant_write_data(function)
