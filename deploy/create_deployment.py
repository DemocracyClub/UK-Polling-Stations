import os
import sys
import time

import boto3

session = boto3.Session(region_name=os.environ.get("AWS_REGION"))


def get_deployment_config_name(code_deploy_client):
    deployment_group = code_deploy_client.get_deployment_group(
        applicationName="WDIVCodeDeploy",
        deploymentGroupName="WDIVDefaultDeploymentGroup",
    )
    asg_name = deployment_group["deploymentGroupInfo"]["autoScalingGroups"][0]["name"]
    autoscale_client = session.client(
        "autoscaling", region_name=os.environ.get("AWS_REGION")
    )

    asgs = autoscale_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[asg_name]
    )

    if len(asgs["AutoScalingGroups"]) == 0:
        return "CodeDeployDefault.AllAtOnce"

    asg_info = asgs["AutoScalingGroups"][0]
    instance_count = len(
        [i for i in asg_info["Instances"] if i["LifecycleState"] == "InService"]
    )
    if instance_count > 1:
        return "CodeDeployDefault.HalfAtATime"
    return "CodeDeployDefault.AllAtOnce"


def create_deployment():
    """
    Create a new deployment and return deploy ID
    """
    client = session.client("codedeploy")
    other_deploys = None
    while other_deploys is not False:
        active_deployments = client.list_deployments(
            includeOnlyStatuses=["Created", "Queued", "InProgress"],
            applicationName="WDIVCodeDeploy",
            deploymentGroupName="WDIVDefaultDeploymentGroup",
        )["deployments"]
        other_deploys = bool(active_deployments)
        if other_deploys:
            WAIT_SECONDS = 60
            print(
                f"Another deploy ({active_deployments}) is blocking this one, waiting {WAIT_SECONDS} seconds"
            )
            time.sleep(WAIT_SECONDS)
    deployment = client.create_deployment(
        applicationName="WDIVCodeDeploy",
        deploymentGroupName="WDIVDefaultDeploymentGroup",
        ignoreApplicationStopFailures=True,
        deploymentConfigName=get_deployment_config_name(client),
        revision={
            "revisionType": "GitHub",
            "gitHubLocation": {
                "repository": "DemocracyClub/UK-Polling-Stations",
                "commitId": os.environ.get("COMMIT_SHA"),
            },
        },
        # When bootstrapping deployment group uncomment this line for the first deploy:
        # ignoreApplicationStopFailures=True,
    )
    return deployment["deploymentId"]


def delete_asg(asg_name):
    """
    Deletes an AutoScalingGroup and all associated instances
    """
    client = session.client("autoscaling")
    return client.delete_auto_scaling_group(
        AutoScalingGroupName=asg_name, ForceDelete=True
    )


def check_deployment(deployment_id):
    """
    Checks the status of the deployment every 60 seconds,
    returns a success or error code
    """
    client = session.client("codedeploy")
    deployment = client.get_deployment(deploymentId=deployment_id)["deploymentInfo"]

    if deployment["status"] == "Succeeded":
        print("SUCCESS")
        exit(0)

    if deployment["status"] in ["Failed", "Stopped"]:
        print("FAIL")
        print(deployment["errorInformation"])
        try:
            summarise_failure(client, deployment_id)

        except Exception:
            # This is some optional logging, so no sweat if it fails
            pass

        # delete the ASG that was created during the failed deployment
        delete_asg(asg_name=deployment["targetInstances"]["autoScalingGroups"][0])
        exit(1)

    print(deployment["status"])
    time.sleep(20)
    check_deployment(deployment_id=deployment_id)


def summarise_failure(deploy_client, deployment_id):
    """
    Get the failure reasons for failed deployments
    """
    failed_target_info = get_failed_target_info(deploy_client, deployment_id)
    failed_event = [
        lce
        for lce in failed_target_info["instanceTarget"]["lifecycleEvents"]
        if lce["status"] == "Failed"
    ][0]
    sys.stdout.write(f"Failed Event: {failed_event['lifecycleEventName']}")
    sys.stdout.write(
        f"Duration {(failed_event['endTime'] - failed_event['startTime']).total_seconds()}"
    )
    sys.stdout.write(f"Diagnostics: {failed_event['diagnostics']}")


def get_failed_target_info(deploy_client, deploy_id):
    """
    returns target_info for a single failed target
    """
    targets = deploy_client.list_deployment_targets(deploymentId=deploy_id)
    target_infos = deploy_client.batch_get_deployment_targets(
        deploymentId=deploy_id, targetIds=targets["targetIds"]
    )
    failed_targets = [
        t
        for t in target_infos["deploymentTargets"]
        if t["instanceTarget"]["status"] == "Failed"
    ]
    return failed_targets[0]


def main():
    deployment_id = create_deployment()
    check_deployment(deployment_id=deployment_id)


if __name__ == "__main__":
    main()
