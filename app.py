import aws_cdk as cdk
from infra.stacks.dev_stack import DevStack

app = cdk.App()

DevStack(app)

app.synth()
