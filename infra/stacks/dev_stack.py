import aws_cdk as cdk
from aws_cdk import pipelines as pipelines
from aws_cdk.pipelines import CodePipelineSource
from constructs import Construct
from lambda_forge import Steps, context

from infra.stages.deploy import DeployStage


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
                    "pip install b_aws_websocket_api==2.0.0",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth",
                ],
            ),
            pipeline_name=f"{context.stage}-{context.name}-Pipeline",
        )

        steps = Steps(self, context, source)

        
        content = """
# Documentation Hub

Welcome to our Documentation Hub! This Markdown file serves as a central hub for accessing all our project documentation. Here, you'll find links to various documents, guides, and resources to help you navigate and understand our project better.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [User Guides](#user-guides)
4. [API Documentation](#api-documentation)
5. [FAQs](#faqs)
6. [Troubleshooting](#troubleshooting)
7. [Contributing Guidelines](#contributing-guidelines)
8. [Code of Conduct](#code-of-conduct)
9. [License](#license)

## Introduction

Provide a brief overview of the project and its purpose. This section should give readers a high-level understanding of what the project is about and why it exists.

## Getting Started

This section should contain resources and guides for users who are new to the project and want to get started. Include installation instructions, system requirements, and any other information necessary to set up the project.

## User Guides

Here, users can find detailed guides on how to use various features of the project. Each guide should be comprehensive and easy to follow, providing step-by-step instructions and examples where necessary.

## API Documentation

If your project has an API, provide detailed documentation here. Include information on endpoints, request and response formats, authentication methods, and any other relevant details.

## FAQs

Compile a list of frequently asked questions along with their answers. This section can help users quickly find solutions to common issues or queries.

## Troubleshooting

In this section, provide troubleshooting tips and solutions for common problems users might encounter while using the project. Include error messages, possible causes, and recommended solutions.

## Contributing Guidelines

If you welcome contributions to your project, include guidelines for contributors here. Explain how users can contribute code, report bugs, or suggest improvements to the project.

## Code of Conduct

Provide a code of conduct that sets the tone for interactions within the project community. This code should outline expected behavior and consequences for violations.

## License

Specify the project's license and include any additional terms or conditions. Make sure users understand their rights and obligations when using or modifying the project.
"""
        wikis = [{
            "title": "Dev",
            "content": content,
            "favicon": "https://docs.lambda-forge.com/images/favicon.png",
        }]
        generate_docs = steps.generate_docs(wikis=wikis)

        pipeline.add_stage(DeployStage(self, context), pre=[generate_docs])


