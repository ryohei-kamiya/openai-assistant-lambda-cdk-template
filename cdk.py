import os
from pathlib import Path
from constructs import Construct
from aws_cdk import App, Stack, Environment, Duration, CfnOutput
from aws_cdk.aws_lambda \
    import DockerImageFunction, DockerImageCode, \
    Architecture, FunctionUrlAuthType
from dotenv import load_dotenv

load_dotenv()


class AssistantDemoTemplateStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_fn = DockerImageFunction(
            self,
            "AssistantDemoTemplateApp",
            code=DockerImageCode.from_image_asset(
                str(Path.cwd()), file="Dockerfile"),
            architecture=self.get_architecture(
                os.environ.get("LAMBDA_ARCHITECTURE", "x86_64")
            ),
            memory_size=int(os.environ.get("LAMBDA_MEMORY_SIZE", 2048))
            if os.environ.get("LAMBDA_MEMORY_SIZE") else 2048,
            timeout=Duration.seconds(
                int(os.environ.get("LAMBDA_TIMEOUT_SEC", 120))
                if os.environ.get("LAMBDA_TIMEOUT_SEC") else 120
            ),
            environment={
                "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
                "OPENAI_ASSISTANT_ID": os.environ.get(
                    "OPENAI_ASSISTANT_ID", ""
                ),
                "APP_HOST": os.environ.get("APP_HOST", ""),
                "APP_PORT": os.environ.get("APP_PORT", ""),
                "APP_USERNAME": os.environ.get("APP_USERNAME", ""),
                "APP_PASSWORD": os.environ.get("APP_PASSWORD", ""),
            }
        )
        fn_url = lambda_fn.add_function_url(
            auth_type=FunctionUrlAuthType.NONE
        )
        CfnOutput(self, "functionUrl", value=fn_url.url)

    def get_architecture(self, architecture: str) -> Architecture:
        if architecture.lower() == "arm64":
            return Architecture.ARM_64
        return Architecture.X86_64


app = App()
stack = AssistantDemoTemplateStack(
    app,
    "AssistantDemoTemplateStack",
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"]
    )
)
app.synth()
