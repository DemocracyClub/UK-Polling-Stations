import os
import time

import boto3
from botocore.exceptions import ClientError

session = boto3.Session(region_name=os.environ.get("AWS_REGION"))

# hardcoded to name in wdiv_stack.py
TARGET_GROUP_NAME = "wdiv-alb-tg"


def check_deployment_group():
    """
    Attempt to get default deployment group.
    TODO allow this to accept args
    """
    client = session.client("codedeploy")
    return client.get_deployment_group(
        applicationName="WDIVCodeDeploy",
        deploymentGroupName="WDIVDefaultDeploymentGroup",
    )


def get_subnet_ids():
    """
    Returns a list of all subnet ids in the AWS account
    """
    client = session.client("ec2")
    response = client.describe_subnets()
    return [subnet["SubnetId"] for subnet in response["Subnets"]]


def get_target_group_arn():
    """
    Returns the arn of the ELB target group defined in sam-template.yaml
    """
    client = session.client("elbv2")
    response = client.describe_target_groups(Names=[TARGET_GROUP_NAME])
    return response["TargetGroups"][0]["TargetGroupArn"]


def create_default_asg():
    """
    Get or create the default auto scaling group
    """
    client = session.client("autoscaling")
    subnet_ids = get_subnet_ids()
    target_group_arn = get_target_group_arn()

    return client.create_auto_scaling_group(
        AutoScalingGroupName="default",
        AvailabilityZones=[
            "eu-west-2a",
            "eu-west-2b",
            "eu-west-2c",
        ],
        LaunchTemplate={"LaunchTemplateName": "wdiv", "Version": "$Latest"},
        MinSize=1,
        MaxSize=1,
        DesiredCapacity=1,
        HealthCheckType="ELB",
        HealthCheckGracePeriod=300,
        TargetGroupARNs=[target_group_arn],
        Tags=[
            {"Key": "CodeDeploy"},
            {"Key": "dc-product", "Value": "wdiv"},
            {
                "Key": "dc-environmnet",
                "Value": os.environ.get("DC_ENVIRONMENT"),
            },
        ],
        TerminationPolicies=[
            "OldestLaunchConfiguration",
            "ClosestToNextInstanceHour",
        ],
        VPCZoneIdentifier=",".join(subnet_ids),
    )


def get_service_role():
    """
    Use IAM client to return details of the CodeDeployServiceRole
    """
    client = boto3.client("iam")
    response = client.get_role(RoleName="CodeDeployServiceRole")
    return response["Role"]


def create_deployment_group():
    """
    Creates a default deployment group in CodeDeploy
    """
    client = session.client("codedeploy")
    service_role = get_service_role()
    return client.create_deployment_group(
        applicationName="WDIVCodeDeploy",
        deploymentGroupName="WDIVDefaultDeploymentGroup",
        autoScalingGroups=[
            "default",
        ],
        deploymentConfigName="CodeDeployDefault.AllAtOnce",
        serviceRoleArn=service_role["Arn"],
        deploymentStyle={
            "deploymentType": "BLUE_GREEN",
            "deploymentOption": "WITH_TRAFFIC_CONTROL",
        },
        blueGreenDeploymentConfiguration={
            "terminateBlueInstancesOnDeploymentSuccess": {
                "action": "TERMINATE",
                "terminationWaitTimeInMinutes": 0,
            },
            "deploymentReadyOption": {
                "actionOnTimeout": "CONTINUE_DEPLOYMENT",
                # 'waitTimeInMinutes': 0
            },
            "greenFleetProvisioningOption": {"action": "COPY_AUTO_SCALING_GROUP"},
        },
        loadBalancerInfo={
            "targetGroupInfoList": [{"name": TARGET_GROUP_NAME}],
        },
    )


def main():
    # check if we have a deployment group already, if so then we
    # assume codedeploy is already configured and nothing to do
    try:
        return check_deployment_group()
    except ClientError:
        pass

    # an error means this is likely the initial setup of a new account
    # so create the default ASG
    create_default_asg()
    # then create the default deployment group using that ASG
    create_deployment_group()
    # as this is an initial deployment wait a minute before moving on to next
    # step as the instance needs to have initialised and be in ready state
    # before code deploy can create a start deployment
    time.sleep(60)
    return None


if __name__ == "__main__":
    main()
