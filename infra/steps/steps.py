from aws_cdk import pipelines as pipelines
from aws_cdk import aws_codebuild as codebuild
from infra.steps import create_step


class Steps:
    def __init__(self, scope, context, source):
        self.scope = scope
        self.context = context
        self.source = source

    def run_unit_tests(self):

        report_group = {
            "scope": self.scope,
            "name": f"{self.context.stage}-{self.context.name}-UnitTestsReport",
            "files": "test-results.xml",
            "base-directory": "pytest-report",
            "file-format": "JUNITXML",
        }

        return create_step(
            source=self.source,
            name=f"{self.context.stage}-{self.context.name}-UnitTests",
            commands=['pytest --junitxml=pytest-report/test-results.xml -k "unit.py"'],
            report_group=report_group,
        )
