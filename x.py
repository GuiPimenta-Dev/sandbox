from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigatewayv2 as apigwv2
from aws_cdk import aws_apigatewayv2_integrations as apigwv2_integrations
from aws_cdk.aws_lambda import Runtime

class MyWebSocketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Lambda function that will handle WebSocket connections
        handler = _lambda.Function(
            self, 'WebSocketHandler',
            runtime=Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'), # Assuming your Lambda code is in the 'lambda' directory
            handler='handler.main', # Assuming your Lambda handler function is named 'main' in 'handler.py'
        )

        # Define the WebSocket API
        api = apigwv2.WebSocketApi(
            self, 'MyWebSocketApi',
            connect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2_integrations.WebSocketLambdaIntegration(
                    handler=handler,
                ),
            ),
        )

        # Deploy the API
        apigwv2.WebSocketStage(
            self, 'DevStage',
            web_socket_api=api,
            stage_name='dev',
            auto_deploy=True,
        )

        # Output the WebSocket URL
        core.CfnOutput(
            self, 'WebSocketURL',
            value=f'wss://{api.api_id}.execute-api.{self.region}.amazonaws.com/dev'
        )

# Remember to replace 'app' with your CDK app instance if necessary
app = core.App()
MyWebSocketStack(app, "MyWebSocketStack")
app.synth()
