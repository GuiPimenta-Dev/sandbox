
from aws_cdk import (
    aws_apigatewayv2 as apiv2,

)

class Websockets:
    def __init__(self, scope, context) -> None:
        self.scope = scope
        self.context = context

    def create_websocket(
        self, name, function, connect_function=None, disconnect_function=None
    ):
        if connect_function is None:
            connect_function = function

        if disconnect_function is None:
            disconnect_function = function

        websocketgw = apiv2.CfnApi(
            self.scope,
            f"{self.context.stage}-{name}-WebSocket",
            name=f"{self.context.stage}-{name}-WebSocket",
            protocol_type="WEBSOCKET",
            route_selection_expression="$request.body.action",
        )

        connect_integration = apiv2.CfnIntegration(
            self.scope,
            f"{self.context.stage}-{name}-ConnectIntegration",
            api_id=websocketgw.ref,
            description=f"{self.context.stage}-{name}-ConnectIntegration",
            integration_type="AWS_PROXY",
            integration_uri=f"arn:aws:apigateway:{self.context.region}:lambda:path/2015-03-31/functions/{connect_function.function_arn}/invocations",
        )

        connect_route = apiv2.CfnRoute(
            self.scope,
            f"{self.context.stage}-{name}-ConnectRoute",
            api_id=websocketgw.ref,
            route_key="$connect",
            authorization_type="NONE",
            operation_name=f"{self.context.stage}-{name}-ConnectRoute",
            target=f"integrations/{connect_integration.ref}",
        )

        import hashlib
        import json
        

        config_hash = hashlib.md5(
        json.dumps({
            # Include any relevant parts of your configuration that, when changed, should trigger a redeployment
            "connect_function_arn": connect_function.function_arn,
            # Add other configurations as needed
        }, sort_keys=True).encode()
    ).hexdigest()
        
        deployment_id = f"WebSocketDeployment{config_hash[:8]}"  # Use part of the hash to keep the ID manageable


        

        deployment = apiv2.CfnDeployment(
            self.scope,
            deployment_id,
            api_id=websocketgw.ref,
        )
        deployment.add_depends_on(connect_route)

        stage = apiv2.CfnStage(self.scope, 
            f"{self.context.stage}-{name}-WSSStage",
            stage_name= self.context.stage.lower(),
            description= f"{self.context.stage}-{name}-WSSStage",
            api_id = websocketgw.ref,
        )
        stage.add_depends_on(connect_route)


        websocket_url = f"wss://{websocketgw.attr_api_endpoint}"

        return websocket_url


       