import json
from pathlib import Path

import typing
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as aws_lambda,
    aws_lambda_python as aws_lambda_python,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_ssm as ssm,
)
from aws_cdk.core import Stack, Duration, Environment
from constructs import Construct

MONITORING_ACCOUNTS = {"development": "985364114241"}


class WDIVS3TriggerStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        env: typing.Union[Environment, typing.Dict[str, typing.Any]],
        **kwargs,
    ) -> None:
        super().__init__(scope, id=id, env=env, **kwargs)

        self.dc_environment = self.node.try_get_context("dc-environment")
        self.account_id = env.account

        uploads_bucket = s3.Bucket.from_bucket_name(
            self,
            f"pollingstations.uploads.{self.dc_environment}_id",
            f"pollingstations.uploads.{self.dc_environment}",
        )

        role = self.create_lambda_role()

        lambda_env_vars = self.get_lambda_env_vars()
        wdiv_s3_trigger_function = aws_lambda_python.PythonFunction(
            self,
            "wdiv_s3_trigger_function",
            function_name="wdiv-s3-trigger",
            entry="cdk/lambdas/wdiv-s3-trigger",
            index="trigger/handler.py",
            handler="main",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.minutes(10),
            role=role,
            environment=lambda_env_vars,
            memory_size=1024,
        )

        uploads_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(wdiv_s3_trigger_function)
        )

    def get_lambda_env_vars(self):
        return {
            "TEMP_BUCKET_NAME": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/TEMP_BUCKET_NAME"
            ),
            "FINAL_BUCKET_NAME": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/FINAL_BUCKET_NAME"
            ),
            "SENTRY_DSN": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/SENTRY_DSN"
            ),
            "GITHUB_REPO": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/GITHUB_REPO"
            ),
            "GITHUB_API_KEY": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/GITHUB_API_KEY"
            ),
            "WDIV_API_KEY": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/WDIV_API_KEY"
            ),
            "ERROR_REPORT_EMAIL": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/ERROR_REPORT_EMAIL"
            ),
            "WDIV_WEBHOOK_URL": ssm.StringParameter.value_for_string_parameter(
                self, "/wdiv_s3_trigger/WDIV_WEBHOOK_URL"
            ),
        }

    def get_policy_json(self):
        json_string = (
            (Path(__file__).parent / "policies/wdiv_s3_trigger_permissions.json")
            .open()
            .read()
        )
        json_string = json_string.replace("{{ACCOUNT_ID}}", self.account_id)
        return json.loads(json_string)

    def create_lambda_role(self):
        role = iam.Role(
            self,
            "wdiv-s3-trigger-lambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            max_session_duration=Duration.hours(1),
        )

        wdiv_s3_trigger_policy_json = self.get_policy_json()

        wdiv_s3_trigger_policy = iam.Policy(
            self,
            "wdiv_s3_trigger_policy_id",
            document=iam.PolicyDocument.from_json(wdiv_s3_trigger_policy_json),
            policy_name="wdiv_s3_trigger_policy",
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
        role.attach_inline_policy(wdiv_s3_trigger_policy)

        return role
