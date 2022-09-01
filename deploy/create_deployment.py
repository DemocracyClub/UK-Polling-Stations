import os
import boto3
import time

session = boto3.Session()


def create_deployment():
    """
    Create a new deployment and return deploy ID
    """
    client = session.client("codedeploy")
    deployment = client.create_deployment(
        applicationName="WDIVCodeDeploy",
        deploymentGroupName="WDIVDefaultDeploymentGroup",
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
    Checks the status of the deploy every 5 seconds,
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
        # delete the ASG that was created during the failed deployment
        delete_asg(asg_name=deployment["targetInstances"]["autoScalingGroups"][0])
        exit(1)

    print(deployment["status"])
    time.sleep(10)
    check_deployment(deployment_id=deployment_id)


def main():
    deployment_id = create_deployment()
    check_deployment(deployment_id=deployment_id)


if __name__ == "__main__":
    main()
