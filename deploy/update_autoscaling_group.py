import os
import time
from collections import defaultdict

import boto3

session = boto3.Session(region_name=os.environ.get("AWS_REGION"))
client = session.client("autoscaling")


def _filter_by_code_deploy_tag(asg):
    """
    Checks if an autoscaling group has CodeDeploy tag
    """
    for tag in asg["Tags"]:
        return tag["Key"] == "CodeDeploy"
    return None


def get_latest_code_deploy_tagged_asg():
    """
    Gets all autoscaling groups, filters them to only those with the
    CodeDeploy tag and returns the most recent one
    """
    asgs = client.describe_auto_scaling_groups()["AutoScalingGroups"]
    asgs = list(filter(_filter_by_code_deploy_tag, asgs))
    asgs.sort(reverse=True, key=lambda asg: asg["CreatedTime"])
    return asgs[0]


def update_asg(asg):
    """
    Updates the number of instances in an autoscaling group
    """
    return client.update_auto_scaling_group(
        AutoScalingGroupName=asg["AutoScalingGroupName"],
        MinSize=int(os.environ.get("MIN_SIZE")),
        MaxSize=int(os.environ.get("MAX_SIZE")),
        DesiredCapacity=int(os.environ.get("DESIRED_CAPACITY")),
    )


def check_asg_instances_healthy(asg):
    """
    Checks the health and lifecycle states of instances in an
    autoscaling group.
    """
    asg = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[asg["AutoScalingGroupName"]]
    )["AutoScalingGroups"][0]

    states = defaultdict(set)
    for instance in asg["Instances"]:
        states["health"].add(instance["HealthStatus"])
        states["lifecycle"].add(instance["LifecycleState"])

    if states == {"health": {"Healthy"}, "lifecycle": {"InService"}}:
        print("All instances healthy and inservice")
        exit(0)

    time.sleep(10)
    check_asg_instances_healthy(asg=asg)
    # TODO let circleci timeout when no output? alternatives e.g. catch error states?


def main():
    asg = get_latest_code_deploy_tagged_asg()
    update_asg(asg=asg)
    print("ASG updated, waiting for all instances to become healthy...")
    check_asg_instances_healthy(asg=asg)


if __name__ == "__main__":
    main()
