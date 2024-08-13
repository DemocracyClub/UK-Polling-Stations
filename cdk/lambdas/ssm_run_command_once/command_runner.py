"""
Uses AWS SSM's Run Command to pick a single instance and run the command given.

This ensures that commands are only ever run once, no matter how many instances are in the TargetGroup (as long as there
is at least one instance)

Commands are run on the instance itself, meaning that the instance needs to have script files and libraries installed
before running.

Think of this as "cron, but not running on every instance"

"""

import random
import time

import boto3


class RunOncePerTagRunCommandClient:
    AWS_REGION = "eu-west-2"

    def __init__(self, tag_name: str, tag_value: str):
        self.tag_value = tag_value
        self.tag_name = tag_name
        self.ssm_client = boto3.client("ssm", region_name=self.AWS_REGION)
        self.ec2_client = boto3.client("ec2", region_name=self.AWS_REGION)

    def _get_single_instance_id_by_tag(
        self, tag_name: str, tag_value: str, region="eu-west-2"
    ) -> str:
        response = self.ec2_client.describe_instances(
            Filters=[
                {"Name": f"tag:{tag_name}", "Values": [tag_value]},
                {
                    "Name": "instance-state-name",
                    "Values": [
                        "running",
                    ],
                },
            ]
        )
        if response:
            instances = response["Reservations"][0]["Instances"]
            random_instance = random.choice(instances)
            self.instance_id = random_instance["InstanceId"]
            return self.instance_id
        raise ValueError(f"No instances found with {tag_name=} and {tag_value=}")

    def run_command_on_single_instance(self, command: str):
        self._get_single_instance_id_by_tag(self.tag_name, self.tag_value)
        self.command_invocation = self.ssm_client.send_command(
            InstanceIds=[self.instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [command]},
            CloudWatchOutputConfig={
                "CloudWatchLogGroupName": "/aws/ssm/command_runner",
                "CloudWatchOutputEnabled": True,
            },
        )
        return self.command_invocation

    def poll_response(self):
        time.sleep(1)
        command_id = self.command_invocation["Command"]["CommandId"]
        print(self.command_invocation)
        status = None
        while status not in ["Success", "Failed"]:
            response = self.ssm_client.get_command_invocation(
                CommandId=command_id, InstanceId=self.instance_id
            )
            status = response["Status"]
            if status == "Success":
                print("Command Succeeded!")
                print(response["StandardOutputContent"])
            if status == "Failed":
                print("Command Failed...")
                print(response)
                print(f"Stderr:{response['StandardErrorContent']}")
                print(f"Stdout:{response['StandardOutputContent']}")
                raise ValueError("Command failed")


if __name__ == "__main__":
    # Use for debugging and ad-hoc commands
    runner = RunOncePerTagRunCommandClient(tag_name="dc-product", tag_value="wdiv")
    runner.run_command_on_single_instance("ls -la /")
    runner.poll_response()
