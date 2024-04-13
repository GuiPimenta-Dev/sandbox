from aws_cdk import aws_lambda as _lambda
from lambda_forge import Path


class Layers:
    def __init__(self, scope) -> None:

        self.pyjwt_layer = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="JWTLayer",
            layer_version_arn="arn:aws:lambda:us-east-2:770693421928:layer:Klayers-p39-PyJWT:3",
        )

        self.sm_utils_layer = _lambda.LayerVersion(
            scope,
            id="SmUtilsLayer",
            code=_lambda.Code.from_asset(Path.layer("layers/sm_utils")),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="",
        )
