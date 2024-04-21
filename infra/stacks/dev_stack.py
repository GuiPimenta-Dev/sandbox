import aws_cdk as cdk
from aws_cdk import pipelines as pipelines
from aws_cdk.pipelines import CodePipelineSource
from constructs import Construct
from infra.stages.deploy import DeployStage
from lambda_forge import context

from infra.steps.steps import Steps


@context(stage="Dev", resources="dev")
class DevStack(cdk.Stack):
    def __init__(self, scope: Construct, context, **kwargs) -> None:
        super().__init__(scope, f"{context.stage}-{context.name}-Stack", **kwargs)

        source = CodePipelineSource.git_hub(f"{context.repo['owner']}/{context.repo['name']}", "dev")

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=source,
                install_commands=[
                    "pip install lambda-forge --extra-index-url https://pypi.org/simple --extra-index-url https://test.pypi.org/simple/",
                    "pip install aws-cdk-lib",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth",
                ],
            ),
            pipeline_name=f"{context.stage}-{context.name}-Pipeline",
        )

        steps = Steps(self, context, source)

        run_unit_tests = steps.run_unit_tests()
        run_coverage = steps.run_coverage()
        validate_integration_tests = steps.validate_integration_tests()
        validate_docs = steps.validate_docs()
        swagger = steps.swagger()
        redoc = steps.redoc()
        diagram = steps.diagram()
        run_integration_tests = steps.run_integration_tests()
        test_report = steps.test_report()
        coverage_report = steps.coverage_report()
        
        pipeline.add_stage(
            DeployStage(self, context),
            pre=[run_unit_tests, run_coverage, validate_docs, validate_integration_tests, swagger, redoc, diagram, test_report, coverage_report],
            post=[run_integration_tests],
        )
