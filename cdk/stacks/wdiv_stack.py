import json
from pathlib import Path

import typing
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_certificatemanager as acm,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    aws_codedeploy as codedeploy,
    aws_ssm as ssm,
    aws_route53 as route_53,
)
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins
import aws_cdk.aws_route53_targets as route_53_target

from aws_cdk.core import Stack, Duration, Environment
from constructs import Construct

# import sys
#
# sys.path.append("..")

EE_IMAGE = "ami-014a706cddda2a79a"
MONITORING_ACCOUNTS = {
    "development": "985364114241",
    "staging": "985364114241",
    "production": "488745607445",
}


class WDIVStack(Stack):
    # TODO
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
        self.latest_ami = ec2.MachineImage.generic_linux(
            ami_map={"eu-west-2": EE_IMAGE}
        )

        self.create_parameters()

        self.policies = self.create_policies()

        self.roles = self.create_roles()

        # self.security_group = self.setup_security_group()
        self.alb_security_group = self.create_alb_security_group()

        self.instance_security_group = self.create_instance_security_group()

        self.wdiv_alb_tg = self.create_wdiv_alb_tg()

        self.launch_template = self.create_launch_template()

        self.alb = self.create_alb(self.subnets, self.wdiv_alb_tg)

        codedeploy.ServerApplication(
            self, "CodeDeployApplicationID", application_name="WDIVCodeDeploy"
        )

        self.create_cloudfront(self.alb)

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
            deregistration_delay=Duration.seconds(60),
        )
        return wdiv_alb_tg

    def create_launch_template(self) -> ec2.LaunchTemplate:
        # Tested high traffic instance. Only use this or larger.
        # c* types suggested as the app is CPU bound
        instance_types_per_env = {
            "development": "t3a.medium",
            "staging": "t3a.medium",
            "production": "c6a.2xlarge",
        }
        launch_template = ec2.LaunchTemplate(
            self,
            "wdiv-launch-template-id",
            instance_type=ec2.InstanceType(
                instance_types_per_env.get(self.dc_environment)
            ),
            machine_image=self.latest_ami,
            launch_template_name="wdiv",
            role=self.roles["codedeploy-ec2-instance-profile"],
            security_group=self.instance_security_group,
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
            desired_capacity=20,
            min_capacity=1,
            max_capacity=25,
        )

    def create_alb(
        self,
        subnets: ec2.SubnetSelection,
        target_group: elbv2.ApplicationTargetGroup,
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

        http_listener.add_target_groups(
            "http-target-groups-id", target_groups=[target_group]
        )

        return alb

    def create_parameters(self) -> None:
        """If you change any of these calls then the value will be reset
        to whatever the initial value is here and you'll have to go reset it in the console
        """
        ssm.StringParameter(
            self,
            "app-dc-environment-id",
            string_value=self.dc_environment,
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
                        "AmazonSSMManagedInstanceCore",
                    ),
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

    def create_cloudfront(self, alb: elbv2.ApplicationLoadBalancer):
        # Hard code the ARN due to a bug with CDK that means we can't run synth
        # with the placeholder values the SSM interface produces :(
        cert_arns = {
            "development": "arn:aws:acm:us-east-1:356853674636:certificate/587f4682-6350-43d1-9a79-7380d351e1ed",
            "staging": "arn:aws:acm:us-east-1:047316047231:certificate/622bd46c-30ec-45ca-8860-5af5b7d7f9c5",
            "production": "arn:aws:acm:us-east-1:864930021230:certificate/f93c7000-ec11-4e90-a016-7c6e0966bf3b",
        }
        cert = acm.Certificate.from_certificate_arn(
            self,
            "CertArn",
            certificate_arn=cert_arns.get(self.dc_environment),
        )

        fqdn = ssm.StringParameter.value_from_lookup(
            self,
            "FQDN",
        )

        cloudfront_dist = cloudfront.Distribution(
            self,
            "WDIVCloudFront_id",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.LoadBalancerV2Origin(
                    alb,
                    http_port=80,
                    protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                    custom_headers={
                        "X-Forwarded-Host": fqdn,
                        "X-Forwarded-Proto": "https",
                    },
                ),
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cache_policy=cloudfront.CachePolicy(
                    self,
                    "short_cache_not_authenticated_id",
                    default_ttl=Duration.minutes(10),
                    min_ttl=Duration.minutes(0),
                    max_ttl=Duration.minutes(120),
                    enable_accept_encoding_brotli=True,
                    enable_accept_encoding_gzip=True,
                    cookie_behavior=cloudfront.CacheCookieBehavior.all(),
                    query_string_behavior=cloudfront.CacheQueryStringBehavior.all(),
                    header_behavior=cloudfront.CacheHeaderBehavior.allow_list(
                        "x-csrfmiddlewaretoken",
                        "X-CSRFToken",
                        "Accept",
                        "Accept-Language",
                        "Cache-Control",
                        "Referer",
                    ),
                ),
            ),
            additional_behaviors={
                "/static/*": cloudfront.BehaviorOptions(
                    origin=origins.LoadBalancerV2Origin(
                        alb,
                        http_port=80,
                        protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                    ),
                    cache_policy=cloudfront.CachePolicy(
                        self,
                        "long_cache_static_id",
                        default_ttl=Duration.days(2000),
                        min_ttl=Duration.minutes(1),
                        max_ttl=Duration.days(2000),
                        enable_accept_encoding_brotli=True,
                        enable_accept_encoding_gzip=True,
                    ),
                )
            },
            certificate=cert,
            domain_names=[fqdn],
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
        )

        hosted_zone = route_53.HostedZone.from_lookup(
            self, "WDIVDomain_id", domain_name=fqdn, private_zone=False
        )
        route_53.ARecord(
            self,
            "FQDN_A_RECORD_TO_CF",
            zone=hosted_zone,
            target=route_53.RecordTarget.from_alias(
                route_53_target.CloudFrontTarget(cloudfront_dist)
            ),
        )
