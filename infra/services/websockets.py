
from aws_cdk import (
    aws_lambda,
    aws_apigatewayv2 as apiv2,
    aws_iam as iam,
)

class Websockets:
    def __init__(self, scope, context, name=None) -> None:
        self.scope = scope
        self.context = context
        self.name = name or context.name

        self.websocket = apiv2.CfnApi(
            self.scope,
            f"{self.context.stage}-{self.name}-WebSocket",
            name=f"{self.context.stage}-{self.name}-WebSocket",
            protocol_type="WEBSOCKET",
            route_selection_expression="$request.body.action",
        )

        apiv2.CfnStage(self.scope, 
            f"{self.context.stage}-{self.name}-WSSStage",
            stage_name= self.context.stage.lower(),
            description= f"{self.context.stage}-{self.name}-WSSStage",
            api_id = self.websocket.ref,
        )

    def create_route(self, function, route_key="$connect"):

        connect_integration = apiv2.CfnIntegration(
            self.scope,
            f"{self.context.stage}-{route_key}-{self.name}-Integration",
            api_id=self.websocket.ref,
            description=f"{self.context.stage}-{route_key}-{self.name}-Integration",
            integration_type="AWS_PROXY",
            integration_uri=f"arn:aws:apigateway:{self.context.region}:lambda:path/2015-03-31/functions/{function.function_arn}/invocations",
        )

        route = apiv2.CfnRoute(
            self.scope,
            f"{self.context.stage}-{route_key}-Route",
            api_id=self.websocket.ref,
            route_key=route_key,
            authorization_type="NONE",
            operation_name=f"{self.context.stage}-{route_key}-{self.name}-Route",
            target=f"integrations/{connect_integration.ref}",
        )

        deployment = apiv2.CfnDeployment(
            self.scope,
            f"{self.context.stage}-{route_key}-{self.name}-WSSDeployment",
            api_id=self.websocket.ref,
        )
        deployment.add_depends_on(route)

        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["execute-api:ManageConnections"],
                resources=[
                    f"arn:aws:execute-api:{self.context.region}:{self.context.account}:{self.websocket.ref}/*",
                    f"arn:aws:execute-api:{self.context.region}:{self.context.account}:{self.websocket.ref}/{self.context.stage.lower()}/POST/@connections/*",
                ],
            )
        )

        websocket_url = f"wss://{self.websocket.attr_api_endpoint}"

        return websocket_url


       