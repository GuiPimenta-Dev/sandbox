from functions.chat.send_message.config import SendMessageConfig
from functions.chat.broadcast.config import BroadcastConfig
from functions.chat.disconnect.config import DisconnectConfig
from functions.chat.connect.config import ConnectConfig
from functions.chat.config import ChatConfig
from aws_cdk import Stack
from constructs import Construct
from lambda_forge import release

from authorizers.jwt.config import JwtAuthorizerConfig
from functions.auth.signin.config import SigninConfig
from functions.auth.signup.config import SignUpConfig
from functions.hello.config import HelloConfig
from infra.services import Services


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

        # Chat
        SendMessageConfig(self.services)
        DisconnectConfig(self.services)
        ConnectConfig(self.services)
