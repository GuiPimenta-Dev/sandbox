from aws_cdk import aws_apigatewayv2 as apiv2


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
            description= 'prod stage',
            api_id = websocketgw.ref,
        )


        # core.CfnOutput(self,'WebSocketURI',
        #     value = f'wss://{websocketgw.ref}.execute-api.{self.context.region}.amazonaws.com/prod',
        #     description = 'URI of websocket'
        # )

        # websocket = apigateway.WebSocketApi(
        #     self.scope,
        #     f"{self.context.stage}-{name}-WebSocket",
        #     connect_route_options=apigateway.WebSocketRouteOptions(
        #         integration=integrations.LambdaWebSocketIntegration(
        #             handler=connect_handler
        #         )
        #     ),
        #     disconnect_route_options=apigateway.WebSocketRouteOptions(
        #         integration=integrations.LambdaWebSocketIntegration(
        #             handler=disconnect_handler
        #         )
        #     ),
        #     default_route_options=apigateway.WebSocketRouteOptions(
        #         integration=integrations.LambdaWebSocketIntegration(handler=function)
        #     ),
        # )

        # apigateway.WebSocketStage(
        #     self.scope,
        #     f"{self.context.stage}-{name}-WebSocket-Stage",
        #     websocket_api=websocket,
        #     stage_name=self.context.stage.lower(),
        #     auto_deploy=True,
        # )

        # core.CfnOutput(
        #     self,
        #     f"{self.context.stage}-{name}-WebSocket-URL",
        #     value=websocket.api_endpoint,
        # )
