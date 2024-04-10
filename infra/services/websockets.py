
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

        # web_socket_api = apiv2.WebSocketApi(self.scope, f"{self.context.stage}-{name}-WebSocket", 
        #     connect_route_options=apigwv2.WebSocketRouteOptions(
        #     integration=WebSocketLambdaIntegration(f"{self.context.stage}-{name}-ConnectRoute", connect_function),
        #     route_key="$connect"
        # ),
        # disconnect_route_options=apigwv2.WebSocketRouteOptions(
        #     integration=WebSocketLambdaIntegration(f"{self.context.stage}-{name}-DisconnectRoute", disconnect_function),
        #     route_key="$disconnect"
        # ),
        # )

        # web_socket_api = apiv2.CfnApi(self, 'websocket',
        #     name =  'SimpleChatWebSocket',
        #     protocol_type = 'WEBSOCKET',
        #     route_selection_expression = '$request.body.action'
        # )
        # apiv2.WebSocketStage(self.scope, self.context.stage.lower(),
        #     web_socket_api=web_socket_api,
        #     stage_name=self.context.stage.lower(),            
        #     auto_deploy=True
        # )


        # web_socket_api.add_route(
        #     "connect",
        #     integration=WebSocketLambdaIntegration("ConnectIntegration", connect_function)
        # )

        # web_socket_api.add_route(
        #     "sendMessage",
        #     integration=WebSocketLambdaIntegration("SendMessageIntegration", function)
            
        # )

        # web_socket_api.add_route(
        #     "disconnect",
        #     integration=WebSocketLambdaIntegration("DisconnectIntegration", disconnect_function)
        # )
        # Connect route
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
            target="integrations/" + connect_integration.ref,
        )

        # #Disconnect route
        disconnect_integration = apiv2.CfnIntegration(
            self.scope,
            f"{self.context.stage}-{name}-DisconnectIntegration",
            api_id=websocketgw.ref,
            description="Disconnect Integration",
            integration_type="AWS_PROXY",
            integration_uri=f"arn:aws:apigateway:{self.context.region}:lambda:path/2015-03-31/functions/{disconnect_function.function_arn}/invocations",
        )
        disconnect_route = apiv2.CfnRoute(
            self.scope,
            f"{self.context.stage}-{name}-DisconnectRoute",
            api_id=websocketgw.ref,
            route_key="$disconnect",
            authorization_type="NONE",
            operation_name=f"{self.context.stage}-{name}-DisconnectRoute",
            target="integrations/" + disconnect_integration.ref,
        )

        # Send Route
        sendmessage_integration = apiv2.CfnIntegration(
            self.scope,
            f"{self.context.stage}-{name}-SendMessageIntegration",
            api_id=websocketgw.ref,
            description="sendmessage Integration",
            integration_type="AWS_PROXY",
            integration_uri=f"arn:aws:apigateway:{self.context.region}:lambda:path/2015-03-31/functions/{function.function_arn}/invocations",
        )
        sendmessage_route = apiv2.CfnRoute(
            self.scope,
            f"{self.context.stage}-{name}-SendMessageRoute",
            api_id=websocketgw.ref,
            route_key="sendmessage",
            authorization_type="NONE",
            operation_name=f"{self.context.stage}-{name}-SendMessageRoute",
            target="integrations/" + sendmessage_integration.ref,
        )

        deployment = apiv2.CfnDeployment(
            self.scope,
            f"{self.context.stage}-{name}-WSSDeployment",
            api_id=websocketgw.ref,
        )
        deployment.add_depends_on(sendmessage_route)
        deployment.add_depends_on(connect_route)
        deployment.add_depends_on(disconnect_route)

        apiv2.CfnStage(self.scope, 
            f"{self.context.stage}-{name}-WSSStage",
            stage_name= self.context.stage.lower(),
            description= f"{self.context.stage}-{name}-WSSStage",
            api_id = websocketgw.ref,
        )

        websocket_url = f"wss://{websocketgw.attr_api_endpoint}"

        return websocket_url


       