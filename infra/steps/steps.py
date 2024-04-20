from aws_cdk import pipelines as pipelines
from infra.steps.codebuild import CodeBuild


class Steps:
    def __init__(self, scope, context, source):
        self.context = context
        self.codebuild = CodeBuild(scope, context, source)

    def run_unit_tests(self):

        partial_build_spec, permissions = self.codebuild.create_report_group(
            name="UnitTestsReport",
            files="test-results.xml",
            base_directory=".",
            file_format="JUNITXML",
        )

        return self.codebuild.create_step(
            name="UnitTests",
            commands=['pytest --junitxml=test-results.xml -k "unit.py"'],
            partial_build_spec=partial_build_spec,
            permissions=permissions,
        )

    def run_coverage(self):

        partial_build_spec, permissions = self.codebuild.create_report_group(
            name="CoverageReport",
            files="coverage.xml",
            base_directory=".",
            file_format="COBERTURAXML",
        )
        
        commands=[
                'coverage run -m pytest -k "unit.py"',
                f"coverage xml --fail-under={self.context.coverage}",
                "touch coverage.xml",
            ]

        return self.codebuild.create_step(
            name="Coverage",
            commands=commands,
            partial_build_spec=partial_build_spec,
            permissions=permissions,
        )
        
    def validate_docs(self):

        return self.codebuild.create_step(
            name="ValidateDocs",
            commands=[
                "cdk synth",
                "python validate_docs.py",
            ],
        )