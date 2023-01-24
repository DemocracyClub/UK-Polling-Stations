import json
from pathlib import Path

import typing
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    aws_codedeploy as codedeploy,
    aws_ssm as ssm,
)
from aws_cdk.core import Stack, Duration, Environment
from constructs import Construct

# import sys
#
# sys.path.append("..")

MONITORING_ACCOUNTS = {"development": "985364114241"}


class WDIVStack(Stack):
    # TODO
    #   - Uploads buckets
    #   - Data hosting
    #   - Deploy trigger
    #   - widget?

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
        self.monitoring_account_id = MONITORING_ACCOUNTS[self.dc_environment]

        self.default_vpc = ec2.Vpc.from_lookup(
            scope=self, id="default-vpc-id", is_default=True
        )
        self.subnets = ec2.SubnetSelection(
            availability_zones=["eu-west-2a", "eu-west-2b", "eu-west-2c"]
        )
        self.latest_ami = ec2.MachineImage.lookup(
            # name="ukpollingstations 2022-08-24T14-45-46Z",
            name="EEImage_ubuntu*"
        )

        self.policies = self.create_policies()

        self.roles = self.create_roles()

        self.create_parameters()

        # self.security_group = self.setup_security_group()
        self.alb_security_group = self.create_alb_security_group()

        self.instance_security_group = self.create_instance_security_group()

        self.wdiv_alb_tg = self.create_wdiv_alb_tg()

        self.launch_template = self.create_launch_template()

        self.alb = self.create_alb(self.subnets, self.wdiv_alb_tg, https=True)

        codedeploy.ServerApplication(
            self, "CodeDeployApplicationID", application_name="WDIVCodeDeploy"
        )

    def create_wdiv_alb_tg(self) -> elbv2.ApplicationTargetGroup:
        wdiv_alb_tg = elbv2.ApplicationTargetGroup(
            self,
            "wdiv-alb-tg-id",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            health_check=elbv2.HealthCheck(
                enabled=True,
                healthy_threshold_count=2,
                interval=Duration.seconds(100),
                port="traffic-port",
                path="/status_check/",
                protocol=elbv2.Protocol.HTTP,
                timeout=Duration.seconds(5),
                unhealthy_threshold_count=5,
                healthy_http_codes="200",
            ),
            target_group_name="wdiv-alb-tg",
            target_type=elbv2.TargetType.INSTANCE,
            vpc=self.default_vpc,
        )
        return wdiv_alb_tg

    def create_launch_template(self) -> ec2.LaunchTemplate:
        launch_template = ec2.LaunchTemplate(
            self,
            "wdiv-launch-template-id",
            instance_type=ec2.InstanceType("t3a.large"),
            machine_image=self.latest_ami,
            launch_template_name="wdiv",
            role=self.roles["codedeploy-ec2-instance-profile"],
            security_group=self.instance_security_group,
            key_name="wdiv-dev",
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume(
                        ec2.EbsDeviceProps(
                            iops=6000,
                            volume_type=ec2.EbsDeviceVolumeType.GP3,
                            volume_size=100,
                        )
                    ),
                )
            ],
        )
        return launch_template

    def create_instance_security_group(self) -> ec2.SecurityGroup:
        instance_security_group = ec2.SecurityGroup(
            self,
            "instance-security-group",
            vpc=self.default_vpc,
            allow_all_outbound=True,
            security_group_name="Instance Security Group",
            description="Allow HTTP and HTTPS access for an instance from the ALB security group",
        )
        instance_security_group.add_ingress_rule(
            ec2.Peer.security_group_id(self.alb_security_group.security_group_id),
            ec2.Port.tcp(80),
            "HTTP from ALB",
        )
        instance_security_group.add_ingress_rule(
            ec2.Peer.security_group_id(self.alb_security_group.security_group_id),
            ec2.Port.tcp(443),
            "HTTPS from ALB",
        )

        return instance_security_group

    def create_alb_security_group(self) -> ec2.SecurityGroup:
        alb_security_group = ec2.SecurityGroup(
            self,
            "alb-security-group",
            vpc=self.default_vpc,
            allow_all_outbound=True,
            security_group_name="ALB Security Group",
            description="ALB accepts all traffic",
        )
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow HTTP from anywhere"
        )
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow HTTPS from anywhere"
        )
        return alb_security_group

    def setup_security_group(self) -> ec2.SecurityGroup:
        security_group = ec2.SecurityGroup(
            self, "security-group-id", vpc=self.default_vpc, allow_all_outbound=True
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow HTTP from anywhere"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow HTTPS from anywhere"
        )

        return security_group

    def create_asg(self) -> autoscaling.AutoScalingGroup:

        return autoscaling.AutoScalingGroup(
            self,
            "asg-id",
            vpc=self.default_vpc,
            launch_template=self.launch_template,
            desired_capacity=1,
            min_capacity=1,
            max_capacity=10,
        )

    def create_alb(
        self,
        subnets: ec2.SubnetSelection,
        target_group: elbv2.ApplicationTargetGroup,
        https: bool = True,
    ) -> elbv2.ApplicationLoadBalancer:
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "application-load-balancer-id",
            vpc=self.default_vpc,
            vpc_subnets=subnets,
            internet_facing=True,
            security_group=self.alb_security_group,
            ip_address_type=elbv2.IpAddressType.IPV4,
            load_balancer_name="wdiv-alb",
        )

        http_listener = alb.add_listener(
            "http-listener-id", port=80, protocol=elbv2.ApplicationProtocol.HTTP
        )

        if https:
            self.add_https_listener(alb, target_group)
            http_listener.add_action(
                "redirect-http-to-https-id",
                action=elbv2.ListenerAction.redirect(
                    port="443", protocol="HTTPS", permanent=True
                ),
            )
        else:
            http_listener.add_target_groups(
                "http-target-groups-id", target_groups=[target_group]
            )

        return alb

    def add_https_listener(
        self,
        alb: elbv2.ApplicationLoadBalancer,
        target_group: elbv2.ApplicationTargetGroup,
    ) -> None:
        https_listener = alb.add_listener(
            "https-listener-id",
            certificates=[
                elbv2.ListenerCertificate.from_arn(
                    ssm.StringParameter.value_from_lookup(
                        self,
                        "SSL_CERTIFICATE_ARN",
                    )
                )
            ],
            port=443,
            protocol=elbv2.ApplicationProtocol.HTTPS,
            default_action=elbv2.ListenerAction.forward([target_group]),
        )

        https_listener.add_certificates(
            "https-listener-certificates-id",
            [
                elbv2.ListenerCertificate.from_arn(
                    "arn:aws:acm:eu-west-2:356853674636:certificate/92a46f99-e2c4-447a-8aee-c978e00f4393"
                ),
            ],
        )

    def create_parameters(self) -> None:
        """If you change any of these calls then the value will be reset
        to whatever the initial value is here and you'll have to go reset it in the console"""
        ssm.StringParameter(
            self,
            "app-dc-environment-id",
            string_value="development",
            parameter_name="DC_ENVIRONMENT",
            description="The DC_ENVIRONMENT environment variable passed to the app.",
            allowed_pattern="^(env-init|development|staging|production)$",
        )

    def create_policies(self) -> dict[str, iam.Policy]:
        def create_policy(policy_id: str, name: str, doc_path: Path) -> iam.Policy:
            document = json.load((Path(__file__).parent / doc_path).open())
            return iam.Policy(
                self,
                policy_id,
                document=iam.PolicyDocument.from_json(document),
                policy_name=name,
            )

        codedeploy_ec2_permissions_policy = create_policy(
            "codedeploy-ec2-permissions-id",
            "CodeDeploy-EC2-Permissions",
            Path("./policies/codedeploy_ec2_permissions.json"),
        )
        logging_assume_role_statement = iam.PolicyStatement.from_json(
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": f"arn:aws:iam::{self.monitoring_account_id}:role/put-record-from-{self.account_id}",
            }
        )
        codedeploy_ec2_permissions_policy.add_statements(logging_assume_role_statement)

        return {
            "codedeploy-launch-template-permissions": create_policy(
                "codedeploy-launch-template-permissions-id",
                "CodeDeployLaunchTemplatePermissions",
                Path("policies/codedeploy_launch_template.json"),
            ),
            "codedeploy-ec2-permissions": codedeploy_ec2_permissions_policy,
            "codedeploy-and-related-services": create_policy(
                "codedeploy-and-related-services-id",
                "CodeDeployAndRelatedServices",
                Path(
                    "./policies/codedeploy_and_related_services.json"
                ),  # TODO: limit the initial resources section by removing wildcard usage
            ),
            "wdiv-deployer": create_policy(
                "wdiv-deployer-id",
                "WDIVDeployer",
                Path("./policies/wdiv_deployer.json"),
            ),
        }

    def create_roles(self) -> dict[str, iam.Role]:
        roles = {
            "packer-ami-builder-role": iam.Role.from_role_name(
                self,
                id="packer-ami-builder-id",
                role_name="packer-ami-builder",
            ),
            "codedeploy-ec2-instance-profile": iam.Role(
                self,
                "codedeploy-ec2-instance-profile-id",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                role_name="CodeDeployEC2InstanceProfile",
                managed_policies=[
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "AmazonSSMReadOnlyAccess",
                    ),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "CloudWatchAgentServerPolicy",
                    ),
                ],
            ),
            "codedeploy-service-role": iam.Role(
                self,
                "codedeploy-service-role-id",
                assumed_by=iam.ServicePrincipal("codedeploy.amazonaws.com"),
                role_name="CodeDeployServiceRole",
            ),
        }

        roles["codedeploy-ec2-instance-profile"].attach_inline_policy(
            self.policies["codedeploy-ec2-permissions"]
        )
        roles["codedeploy-service-role"].attach_inline_policy(
            self.policies["codedeploy-launch-template-permissions"]
        )
        roles["codedeploy-service-role"].add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "aws-code-deploy-role-id",
                "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole",
            )
        )

        return roles
