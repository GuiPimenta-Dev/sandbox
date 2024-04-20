from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_iam as iam
from aws_cdk import pipelines as pipelines


def create_step(
    source,
    name,
    commands,
    install_commands=[],
    env={},
    partial_build_spec={},
    permissions=[],
    report_group=None,
    requirements="requirements.txt",
):

    PUBLIC_ECR = "public.ecr.aws/x8r4y7j7/lambda-forge-generate-docs"

    ECR_PERMISSIONS = iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        actions=["ecr:*"],
        resources=["*"],
    )

    if report_group:
        report_group_build_spec, report_group_permissions = get_report_group(report_group)
        partial_build_spec.update(report_group_build_spec)
        permissions += report_group_permissions

    return pipelines.CodeBuildStep(
        name,
        input=source,
        install_commands=[
            "forge layer --install",
            f"pip install -r {requirements}",
            *install_commands,
        ],
        env=env,
        commands=commands,
        build_environment=codebuild.BuildEnvironment(
            build_image=codebuild.LinuxBuildImage.from_docker_registry(PUBLIC_ECR),
            privileged=True,
            compute_type=codebuild.ComputeType.SMALL,
            environment_variables=env,
        ),
        partial_build_spec=codebuild.BuildSpec.from_object(partial_build_spec),
        cache=codebuild.Cache.local(codebuild.LocalCacheMode.DOCKER_LAYER, codebuild.LocalCacheMode.CUSTOM),
        role_policy_statements=[ECR_PERMISSIONS, *get_role_policy_statements(permissions)],
    )


def get_role_policy_statements(permissions):
    role_policy_statements = []
    for role in permissions:
        role_policy_statements.append(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=role["actions"],
                resources=role["resources"],
            )
        )

    return role_policy_statements


def get_report_group(report):
    report_group = codebuild.ReportGroup(report["scope"], report["name"])

    report_group_build_spec = {
        "reports": {
            report_group.report_group_arn: {
                "files": report["files"],
                "base-directory": report["base-directory"],
                "file-format": report["file-format"],
            }
        },
    }

    report_group_permissions = [
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

    return report_group_build_spec, report_group_permissions
