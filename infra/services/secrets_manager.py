from aws_cdk import aws_secretsmanager as secrets_manager

        
class SecretsManager:
    def __init__(self, scope, context) -> None:

        self.jwt_secret = secrets_manager.Secret.from_secret_complete_arn(
            scope,
            id="JwtSecret",
            secret_complete_arn="arn:aws:secretsmanager:us-east-2:211125768252:secret:jwt-yx2zBV",
        )