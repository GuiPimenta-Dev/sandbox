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
            coverage=True,
        )

        commands = [
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
            commands=["cdk synth", "python validate_docs.py"],
        )

    def ls(self):

        return self.codebuild.create_step(
            name="ValidateDocs",
            commands=["cdk synth", "ls -la"],
        )

    def validate_integration_tests(self):
        conftest = """import json 
def pytest_generate_tests(metafunc):
    for mark in metafunc.definition.iter_markers(name="integration"):
        with open("tested_endpoints.txt", "a") as f:
            f.write(f"{json.dumps(mark.kwargs)}|")"""

        commands = [
            "cdk synth",
            "rm -rf cdk.out",
            f"echo '{conftest}' > conftest.py",
            "pytest -m integration --collect-only . -q",
            "python validate_integration_tests.py",
        ]

        return self.codebuild.create_step(name="ValidateIntegrationTests", commands=commands)

    def validate_integration_tests(self):
        conftest = """import json 
    def pytest_generate_tests(metafunc):
        for mark in metafunc.definition.iter_markers(name="integration"):
            with open("tested_endpoints.txt", "a") as f:
                f.write(f"{json.dumps(mark.kwargs)}|")"""

        commands = [
            "cdk synth",
            "rm -rf cdk.out",
            f"echo '{conftest}' > conftest.py",
            "pytest -m integration --collect-only . -q",
            "python validate_integration_tests.py",
        ]

        return self.codebuild.create_step(name="ValidateIntegrationTests", commands=commands)

    def run_integration_tests(self):

        partial_build_spec, permissions = self.codebuild.create_report_group(
            name="IntegrationTestsReport",
            files="test-results.xml",
            base_directory=".",
            file_format="JUNITXML",
        )

        return self.codebuild.create_step(
            name="IntegrationTests",
            commands=['pytest --junitxml=pytest-report/test-results.xml -k "integration.py"'],
            partial_build_spec=partial_build_spec,
            permissions=permissions,
        )
