
from b_aws_websocket_api.ws_api import WsApi
from b_aws_websocket_api.ws_stage import WsStage
from b_aws_websocket_api.ws_lambda_integration import WsLambdaIntegration
from b_aws_websocket_api.ws_route import WsRoute
from  b_aws_websocket_api.ws_deployment import WsDeployment


class Websockets:
    def __init__(self, scope, context, name=None) -> None:
        self.scope = scope
        self.context = context
        self.name = name or context.name

        self.websocket = WsApi(
            scope=self.scope,
            id=f"{self.context.stage}-{self.name}-WebSocket",
            name=f"{self.context.stage}-{self.name}-WebSocket",
            route_selection_expression='$request.body.action',
        )

        self.stage = WsStage(
            scope=self.scope,
            id=f"{self.context.stage}-{self.name}-WSS-Stage",
            ws_api=self.websocket,
            stage_name=context.stage.lower(),
            auto_deploy=True,
        )



    def create_route(self, route_key, function ):

        route_key = route_key.replace("$", "")

        integration = WsLambdaIntegration(
            scope=self.scope,
            id=f"{self.context.stage}-{self.name}-Integration-{route_key}",
            integration_name=f"{self.context.stage}-{self.name}-Integration-{route_key}",
            ws_api=self.websocket,
            function=function
        )

        route = WsRoute(
            scope=self.scope,
            id=f"{self.context.stage}-{self.name}-Route-{route_key}",
            ws_api=self.websocket,
            route_key=route_key,
            authorization_type='NONE',
            route_response_selection_expression='$default',
            target=f'integrations/{integration.ref}',
        )

        deployment = WsDeployment(
            scope=self.scope,
            id=f"{self.context.stage}-{self.name}-Deployment-{route_key}",
            ws_stage=self.stage
        )

        deployment.node.add_dependency(route)
        deployment.node.add_dependency(self.stage)

        websocket_url = f"wss://{self.websocket.attr_api_endpoint}"

        return websocket_url


       