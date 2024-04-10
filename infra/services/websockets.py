from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_apigatewayv2_integrations as integrations
from aws_cdk import core


class Websockets:
    def __init__(self, scope, context) -> None:
        self.scope = scope
        self.context = context

    def create_websocket(
        self, name, function, connect_handler=None, disconnect_handler=None
    ):
        if connect_handler is None:
            connect_handler = function

        if disconnect_handler is None:
            disconnect_handler = function

        websocket = apigateway.WebSocketApi(
            self.scope,
            f"{self.context.stage}-{name}-WebSocket",
            connect_route_options=apigateway.WebSocketRouteOptions(
                integration=integrations.LambdaWebSocketIntegration(
                    handler=connect_handler
                )
            ),
            disconnect_route_options=apigateway.WebSocketRouteOptions(
                integration=integrations.LambdaWebSocketIntegration(
                    handler=disconnect_handler
                )
            ),
            default_route_options=apigateway.WebSocketRouteOptions(
                integration=integrations.LambdaWebSocketIntegration(handler=function)
            ),
        )

        apigateway.WebSocketStage(
            self.scope,
            f"{self.context.stage}-{name}-WebSocket-Stage",
            websocket_api=websocket,
            stage_name=self.context.stage.lower(),
            auto_deploy=True,
        )

        core.CfnOutput(
            self,
            f"{self.context.stage}-{name}-WebSocket-URL",
            value=websocket.api_endpoint,
        )
