import aws_cdk.aws_lambda_python_alpha as aws_lambda_python
from aws_cdk import (
    Duration,
    Stack,
    aws_events,
    aws_events_targets,
    aws_iam,
    aws_lambda,
    aws_sns,
    aws_sns_subscriptions,
)
from constructs import Construct


class WDIVOncePerTagCommandRunner(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = aws_iam.Role(
            self,
            "OncePerTagCommandRunnerRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            max_session_duration=Duration.hours(1),
        )
        for managed_policy_arn in [
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
            "arn:aws:iam::aws:policy/AmazonSSMFullAccess",
            "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess",
        ]:
            managed_policy = aws_iam.ManagedPolicy.from_managed_policy_arn(
                self,
                managed_policy_arn.split("/")[-1],
                managed_policy_arn=managed_policy_arn,
            )
            role.add_managed_policy(managed_policy)

        self.once_per_tag_command_runner = aws_lambda_python.PythonFunction(
            self,
            "once_per_tag_command_runner",
            function_name="once_per_tag_command_runner",
            entry="./cdk/lambdas/ssm_run_command_once",
            index="main.py",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            timeout=Duration.minutes(2),
            role=role,
        )

        # Environment conditionals
        dc_environment = self.node.try_get_context("dc-environment") or "development"

        # SNS topic for SSM command failure alerts
        self.ssm_failure_topic = aws_sns.Topic(
            self,
            "SSMCommandFailureTopic",
            topic_name=f"ssm-command-runner-failures-{dc_environment}",
            display_name="SSM Command Runner Failures",
        )
        self.ssm_failure_topic.add_subscription(
            aws_sns_subscriptions.EmailSubscription(
                f"developers+wdiv-ssm-failures-{dc_environment}@democracyclub.org.uk"
            )
        )

        # EventBridge rule to capture SSM command failures and route to SNS
        # https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-systems-manager-events.html
        # https://docs.aws.amazon.com/systems-manager/latest/userguide/monitor-commands.html
        # https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html
        ssm_failure_rule = aws_events.Rule(
            self,
            "SSMCommandFailureRule",
            rule_name=f"ssm-command-runner-failure-alert-{dc_environment}",
            description="Alerts when SSM Run Commands fail on EC2 instances",
            event_pattern=aws_events.EventPattern(
                source=["aws.ssm"],
                detail_type=[
                    "EC2 Command Invocation Status-change Notification",
                    "EC2 Command Status-change Notification",
                ],
                detail={
                    "status": [
                        {
                            "anything-but": [
                                "Pending",
                                "InProgress",
                                "Delayed",
                                "Success",
                            ]
                        }
                    ],
                },
            ),
        )
        ssm_failure_rule.add_target(aws_events_targets.SnsTopic(self.ssm_failure_topic))

        if dc_environment in ["development", "staging", "production"]:
            self.add_job(
                "import_councils_from_ec_on_principal",
                "cron(1 * * * ? *)",
                "/usr/bin/manage-py-command import_councils --only-contact-details --database principal",
            )
            self.add_job(
                "teardown_expired_data",
                "cron(0 3 ? * SUN *)",
                "runuser -l polling_stations -c '/usr/bin/manage-py-command teardown_expired_data'",
            )
            self.add_job(
                "run_once_custom_metrics",
                "rate(5 minutes)",
                "/var/www/polling_stations/run_once_custom_metrics.sh",
            )

        if dc_environment in ["development", "staging", "production"]:
            command = "runuser -l polling_stations -c '/usr/bin/manage-py-command import_eoni_from_s3 --send-slack-report'"
            if dc_environment == "staging":
                # Don't bother to post to bots on staging.
                command = "runuser -l polling_stations -c '/usr/bin/manage-py-command import_eoni_from_s3'"
            self.add_job(
                "import_eoni_data_from_s3",
                "cron(30 1 * * ? *)",
                command,
            )

        if dc_environment in ["development", "staging", "production"]:
            command = "runuser -l polling_stations -c '/usr/bin/manage-py-command drop_failed_replication_slots --send-slack-report'"
            if dc_environment == "staging":
                # Don't bother to post to bots on staging.
                command = "runuser -l polling_stations -c '/usr/bin/manage-py-command drop_failed_replication_slots'"
            self.add_job(
                "drop_failed_replication_slots",
                "cron(30 2 * * ? *)",
                command,
            )

    def add_job(
        self,
        command_name,
        schedule_expression,
        command,
        tag_name="dc-product",
        tag_value="wdiv",
    ):
        _command = aws_events.Rule(
            self,
            command_name,
            rule_name=command_name,
            schedule=aws_events.Schedule.expression(schedule_expression),
        )
        _command.add_target(
            aws_events_targets.LambdaFunction(
                handler=self.once_per_tag_command_runner,
                event=aws_events.RuleTargetInput.from_object(
                    {
                        "tag_name": tag_name,
                        "tag_value": tag_value,
                        "command": command,
                    }
                ),
            )
        )
