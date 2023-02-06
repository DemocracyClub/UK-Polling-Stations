from command_runner import RunOncePerTagRunCommandClient


def handler(event, context):
    tag_name = event["tag_name"]
    tag_value = event["tag_value"]
    command = event["command"]

    runner = RunOncePerTagRunCommandClient(tag_name=tag_name, tag_value=tag_value)
    runner.run_command_on_single_instance(command)
    print(runner.command_invocation)
