from aws_cdk import pipelines as pipelines
from infra.steps.codebuild import CodeBuild


class Steps:
    def __init__(self, scope, context, source):
        self.codebuild = CodeBuild(scope, context, source)

    def run_unit_tests(self):

        partial_build_spec, permissions = self.codebuild.create_report_group(
            name="UnitTestsReport",
            files="test-results.xml",
            base_directory="pytest-report",
            file_format="JUNITXML",
        )

        return self.codebuild.create_step(
            name="UnitTests",
            commands=['pytest --junitxml=pytest-report/test-results.xml -k "unit.py"'],
            partial_build_spec=partial_build_spec,
            permissions=permissions,
        )
