import aws_cdk as cdk
from constructs import Construct

from infra.stacks.lambda_stack import LambdaStack


class DeployStage(cdk.Stage):
    def __init__(self, scope: Construct, context, **kwargs):
        super().__init__(scope, context.stage, **kwargs)

        lambda_stack = LambdaStack(self, context)

        lambda_stack.services.api_gateway.create_docs(authorizer=None)

        lambda_stack.services.api_gateway.create_docs(authorizer=None, endpoint="/wiki", artifact="wiki")

        lambda_stack.services.api_gateway.create_docs(authorizer=None, endpoint="/diagram", artifact="diagram")

        lambda_stack.services.api_gateway.create_docs(authorizer=None, endpoint="/tests", artifact="tests")

        lambda_stack.services.api_gateway.create_docs(authorizer=None, endpoint="/coverage", artifact="coverage")
