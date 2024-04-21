from aws_cdk import pipelines as pipelines
from infra.steps.codebuild import CodeBuild


class Steps:
    def __init__(self, scope, context, source):
        self.context = context
        self.codebuild = CodeBuild(scope, context, source)
        self.s3_permissions = [
            {
                "actions": [
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                ],
                "resources": ["*"],
            }
        ]

    def run_unit_tests(self):

        partial_build_spec, permissions = self.codebuild.create_report_group(
            name="UnitTestsReport",
            files="test-results.xml",
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

        return self.codebuild.create_step(
            name="Coverage",
            partial_build_spec=partial_build_spec,
            permissions=permissions,
            commands=[
                'coverage run -m pytest -k "unit.py"',
                f"coverage xml --fail-under={self.context.coverage}",
                "touch coverage.xml",
            ],
        )

    def validate_docs(self):

        return self.codebuild.create_step(
            name="ValidateDocs",
            commands=["cdk synth", "python validate_docs.py"],
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

        return self.codebuild.create_step(
            name="ValidateIntegrationTests",
            commands=[
                "cdk synth",
                "rm -rf cdk.out",
                f"echo \"{conftest}\" > conftest.py",
                "pytest -m integration --collect-only . -q",
                "python validate_integration_tests.py",
            ],
        )

    def run_integration_tests(self):

        partial_build_spec, permissions = self.codebuild.create_report_group(
            name="IntegrationTestsReport",
            files="test-results.xml",
            file_format="JUNITXML",
        )

        return self.codebuild.create_step(
            name="IntegrationTests",
            partial_build_spec=partial_build_spec,
            permissions=permissions,
            commands=['pytest --junitxml=test-results.xml -k "integration.py"'],
        )

    def swagger(self):
        return self.codebuild.create_step(
            name="Swagger",
            permissions=self.s3_permissions,
            commands=[
                "cdk synth",
                "python generate_docs.py",
                "python swagger_yml_to_ui.py < docs.yaml > swagger.html",
                f"aws s3 cp swagger.html s3://{self.context.bucket}/{self.context.name}/{self.context.stage.lower()}/swagger.html",
            ],
        )

    def redoc(self):
        return self.codebuild.create_step(
            name="Redoc",
            permissions=self.s3_permissions,
            commands=[
                "cdk synth",
                "python generate_docs.py",
                "redoc-cli bundle -o redoc.html docs.yaml",
                f"aws s3 cp redoc.html s3://{self.context.bucket}/{self.context.name}/{self.context.stage.lower()}/redoc.html",
            ],
        )

    def diagram(self):
        return self.codebuild.create_step(
            name="Diagram",
            permissions=self.s3_permissions,
            commands=[
                f"python generate_diagram.py {self.context.stage}",
                "python embed_image_in_html.py diagram.png diagram.html",
                f"aws s3 cp diagram.html s3://{self.context.bucket}/{self.context.name}/{self.context.stage.lower()}/diagram.html",
            ],
        )
    
    def wikis(self, wikis=[]):
        commands = []
        for wiki in wikis:
            file_path = wiki.get("file_path", "")
            title = wiki.get("title", "Wiki").title()
            favicon = wiki.get("favicon", "favicon.png")
            commands.append(f"python generate_wiki.py '{file_path}' '{title}' '{favicon}'")
            commands.append(
                f"aws s3 cp {title}.html s3://{self.context.bucket}/{self.context.name}/{self.context.stage.lower()}/{title.lower()}.html"
            )
            
        return self.codebuild.create_step(
            name="Wikis",
            permissions=self.s3_permissions,
            commands=commands,
        )
    
    def test_report(self):
        return self.codebuild.create_step(
            name="TestReport",
            commands=[
                "pytest --html=report.html --self-contained-html || echo 'skipping failure'",
                f"aws s3 cp report.html s3://{self.context.bucket}/{self.context.name}/{self.context.stage.lower()}/tests.html",
            ],
        )
    
    def coverage_report(self):
        return self.codebuild.create_step(
            name="CoverageReport",
            permissions=self.s3_permissions,
            commands=[
                "coverage run -m pytest --html=report.html --self-contained-html || echo 'skipping failure'",
                "coverage html",
                f"aws s3 cp htmlcov/index.html s3://{self.context.bucket}/{self.context.name}/{self.context.stage.lower()}/coverage.html",
            ],
        )