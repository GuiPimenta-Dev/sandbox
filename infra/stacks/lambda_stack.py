from functions.users.hello.config import HelloConfig
from authorizers.jwt.config import JwtAuthorizerConfig
from functions.users.signin.config import SigninConfig
from aws_cdk import Stack
from constructs import Construct
from functions.users.signup.config import SignUpConfig
from infra.services import Services
from lambda_forge import release


@release
class LambdaStack(Stack):
    def __init__(self, scope: Construct, context, **kwargs) -> None:

        super().__init__(scope, f"{context.name}-Lambda-Stack", **kwargs)

        self.services = Services(self, context)

        # Authorizers
        JwtAuthorizerConfig(self.services)

        # Users
        HelloConfig(self.services)
        SigninConfig(self.services)
        SignUpConfig(self.services)
