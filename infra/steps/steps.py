from aws_cdk import pipelines as pipelines
from aws_cdk import aws_codebuild as codebuild
from infra.steps import create_step


class Steps:
    def __init__(self, scope, context, source):
        self.scope = scope
        self.context = context
        self.source = source

    def run_unit_tests(self):

        report_group = codebuild.ReportGroup(
            self.scope,
            f"{self.context.stage}-{self.context.name}-UnitReportGroup",
        )

        partial_build_spec = {
            "reports": {
                report_group.report_group_arn: {
                    "files": "test-results.xml",
                    "base-directory": "pytest-report",
                    "file-format": "JUNITXML",
                }
            },
        }

        permissions = [
            {
                "actions": [
                    "codebuild:CreateReportGroup",
                    "codebuild:CreateReport",
                    "codebuild:UpdateReport",
                    "codebuild:BatchPutTestCases",
                    "codebuild:BatchPutCodeCoverages",
                ],
                "resources": [report_group.report_group_arn],
            }
        ]

        return create_step(
            source=self.source,
            name=f"{self.context.stage}-{self.context.name}-UnitTests",
            commands=['pytest --junitxml=pytest-report/test-results.xml -k "unit.py"'],
            permissions=permissions,
            partial_build_spec=partial_build_spec,
        )
