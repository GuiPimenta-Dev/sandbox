
from aws_cdk import (
    aws_apigatewayv2 as apiv2,

)
import hashlib
import json

class Websockets:
    def __init__(self, scope, context) -> None:
        self.scope = scope
        self.context = context

        self.websocket = apiv2.CfnApi(
            self.scope,
            f"{self.context.stage}-{context.name}-WebSocket",
            name=f"{self.context.stage}-{context.name}-WebSocket",
            protocol_type="WEBSOCKET",
            route_selection_expression="$request.body.action",
        )

    def create_route(
        self, function
    ):

        connect_integration = apiv2.CfnIntegration(
            self.scope,
            f"{self.context.stage}-{self.context.name}-ConnectIntegration",
            api_id=self.websocket.ref,
            description=f"{self.context.stage}-{self.context.name}-ConnectIntegration",
            integration_type="AWS_PROXY",
            integration_uri=f"arn:aws:apigateway:{self.context.region}:lambda:path/2015-03-31/functions/{function.function_arn}/invocations",
        )

        connect_route = apiv2.CfnRoute(
            self.scope,
            f"{self.context.stage}-{self.context.name}-ConnectRoute",
            api_id=self.websocket.ref,
            route_key="$connect",
            authorization_type="NONE",
            operation_name=f"{self.context.stage}-{self.context.name}-ConnectRoute",
            target=f"integrations/{connect_integration.ref}",
        )


        

        config_hash = hashlib.md5(
        json.dumps({
            # Include any relevant parts of your configuration that, when changed, should trigger a redeployment
            "connect_function_arn": function.function_arn,
            # Add other configurations as needed
        }, sort_keys=True).encode()
    ).hexdigest()
        
        deployment_id = f"WebSocketDeployment{config_hash[:8]}"  # Use part of the hash to keep the ID manageable

        deployment = apiv2.CfnDeployment(
            self.scope,
            deployment_id,
            api_id=self.websocket.ref,
        )
        deployment.add_dependency(connect_route)

        stage = apiv2.CfnStage(self.scope, 
            f"{self.context.stage}-{self.context.name}-WSSStage",
            stage_name= self.context.stage.lower(),
            description= f"{self.context.stage}-{self.context.name}-WSSStage",
            api_id = self.websocket.ref,
        )
        stage.add_dependency(connect_route)

        websocket_url = f"wss://{self.websocket.attr_api_endpoint}"

        return websocket_url


       