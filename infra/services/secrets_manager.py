from aws_cdk import aws_secretsmanager as secrets_manager

        
class SecretsManager:
    def __init__(self, scope, context) -> None:

        # self.secrets_manager = secrets_manager.Secret.from_secret_complete_arn(
        #     scope,
        #     id="SecretsManager",
        #     secret_complete_arn=context.resources["arns"]["secrets_manager_arn"],
        # )
        ...
