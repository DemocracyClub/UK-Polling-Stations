import os
import subprocess
import sys
import warnings
from pathlib import Path

import dotenv
from invoke import task
import boto3

from cdk.lambdas.ssm_run_command_once.command_runner import (
    RunOncePerTagRunCommandClient,
)


def get_ssm_parameter_value(client, key):
    response = client.get_parameter(Name=key)
    return response["Parameter"]["Value"]


def get_rds_connection_string(
    profile,
    user="postgres",
    db_name=None,
    host=None,
    password=None,
):
    session = boto3.session.Session(profile_name=profile)
    ssm_client = session.client("ssm")
    if (db_name := db_name) is None:
        db_name = get_ssm_parameter_value(ssm_client, "RDS_DB_NAME")
    if (host := host) is None:
        host = get_ssm_parameter_value(ssm_client, "RDS_DB_HOST")
    if (password := password) is None:
        password = get_ssm_parameter_value(ssm_client, "RDS_DB_PASSWORD")

    return f"postgresql://{user}:{password}@{host}/{db_name}"


def git_revision():
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"])
        revision = out.strip().decode("ascii")
    except OSError:
        revision = "Unknown"

    return revision


def bootstrap_django():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polling_stations.settings")
    import django

    django.setup()
    sys.path.append(str(Path.cwd() / "polling_stations/apps/"))


@task
def import_eoni(ctx, environment):
    """
    AWS_PROFILE=dev-wdiv-dc inv import-eoni development
    """
    tag_name = "dc-environment"
    tag_value = environment
    command = "runuser -l polling_stations -c '/var/www/polling_stations/import_eoni_from_s3.sh'"
    runner = RunOncePerTagRunCommandClient(tag_name=tag_name, tag_value=tag_value)
    runner.run_command_on_single_instance(command)
    print(runner.command_invocation)
    runner.poll_response()


@task
def import_council(ctx, environment, reg_code):
    """
    AWS_PROFILE=dev-wdiv-dc inv import-council development MDE
    """
    bootstrap_django()
    from councils.models import Council

    council = Council.objects.get(council_id=reg_code)
    import_command = council.import_script_path.split("/")[-1][:-3]
    tag_name = "dc-environment"
    tag_value = environment
    command = (
        f"runuser -l polling_stations -c '/usr/bin/manage-py-command {import_command}'"
    )
    runner = RunOncePerTagRunCommandClient(tag_name=tag_name, tag_value=tag_value)
    runner.run_command_on_single_instance(command)
    print(f"Running {import_command} on {environment}")
    print(runner.command_invocation)
    runner.poll_response()


@task
def teardown_council(ctx, environment, reg_code):
    """
    AWS_PROFILE=dev-wdiv-dc inv teardown-council development BRO
    """
    tag_name = "dc-environment"
    tag_value = environment
    command = f"runuser -l polling_stations -c '/usr/bin/manage-py-command teardown --council {reg_code}'"
    runner = RunOncePerTagRunCommandClient(tag_name=tag_name, tag_value=tag_value)
    runner.run_command_on_single_instance(command)
    print(runner.command_invocation)
    runner.poll_response()


@task
def describe_parameters(ctx, profile=os.environ.get("AWS_PROFILE", None)):
    session = boto3.session.Session(profile_name=profile)
    ssm_client = session.client("ssm")
    for parameter in ssm_client.describe_parameters()["Parameters"]:
        print(
            f"{parameter['Name']} => {get_ssm_parameter_value(ssm_client,parameter['Name'])}"
        )
        print(f"{parameter.get('Description')}")
        print()


@task(
    help={
        "profile": "Required. Name of AWS profile to be called with",
    }
)
def rds_psql(
    ctx, profile, user="postgres", db_name=None, host=None, password=None, print=False
):
    """
    Start psql client to rds associate with <profile> account.
    NB This does not mean the rds is in that account.
    Merely the DB that parameter store points at. i.e. 'stage' might point at a db in 'dev'
    """
    conn_string = get_rds_connection_string(
        profile, user=user, db_name=db_name, host=host, password=password
    )
    if print:
        sys.stdout.write(f"\npsql {conn_string}\n\n")
        return
    ctx.run(f"psql {conn_string}")


@task(
    help={
        "profile": "Required. Name of AWS profile to be called with",
    }
)
def list_rds_dbs(
    ctx,
    profile,
    user="postgres",
    db_name=None,
    host=None,
    password=None,
):
    conn_string = get_rds_connection_string(
        profile, user=user, db_name=db_name, host=host, password=password
    )
    ctx.run(f'psql {conn_string} -c "\l"')


@task(
    help={
        "profile": "Required. Name of AWS profile to be called with",
    }
)
def list_subscriptions(
    ctx,
    profile,
    user="postgres",
    db_name=None,
    host=None,
    password=None,
    fmt="csv",
):
    conn_string = get_rds_connection_string(
        profile, user=user, db_name=db_name, host=host, password=password
    )
    ctx.run(f'psql {conn_string} -c "select * from pg_replication_slots;" --{fmt}')


@task
def list_db_parameters(ctx, profile, name):
    """
    List parameters in parameter group "Name"
    Examples:
         inv list-db-parameters --profile prod-wdiv-dc | jq '.[][] | select(.Source | test("user")) | {ParameterName, ParameterValue, ApplyMethod}'
    """
    ctx.run(
        f"""
        aws --profile {profile} rds describe-db-parameters \
            --db-parameter-group-name {name}"""
    )


@task(
    help={
        "profile": "Required. Name of AWS profile to be called with",
        "output": "Output Format. Defaults to 'table'.  Valid choices: table|json|text|yaml|yaml-stream",
    }
)
def describe_instances(ctx, profile, output="table"):
    """
    Describe EC2 Instances in <profile> aws environment
    Examples:
        inv describe-instances --profile prod-wdiv-dc
        inv describe-instances --profile prod-wdiv-dc --output json | jq '.[][]' | mlr --ijson --oxtab  cat
    """
    query = "Reservations[*].Instances[*].{PublicIP:PublicIpAddress,Type:InstanceType,Name:Tags[?Key=='Name']|[0].Value,InstanceID:InstanceId,Status:State.Name}"

    command = f"""
    aws ec2 describe-instances \
        --profile {profile} \
        --filters "Name=instance-state-name,Values=running" \
        --query "{query}" \
        --output {output}
    """

    ctx.run(command)


def create_deployment(ctx, profile, commit=None):
    """
    Create a CodeDeploy deployment
    """
    if not commit:
        commit = git_revision()

    ctx.run(
        f"AWS_PROFILE={profile} COMMIT_SHA={commit} python deploy/create_deployment.py"
    )


@task(
    help={
        "upgrade": "attempt to upgrade dependencies in line with .in constraint file",
    }
)
def requirements(ctx, upgrade=False):
    """
    Generate various requirements/*.txt files
    """
    paths = {
        "requirements/base.in": "requirements/base.txt",
        "requirements/testing.in": "requirements/testing.txt",
        "requirements/cdk.in": "requirements/cdk.txt",
        "requirements/local.in": "requirements/local.txt",
        "cdk/lambdas/wdiv-s3-trigger/requirements/base.in": "cdk/lambdas/wdiv-s3-trigger/requirements.txt",
        "cdk/lambdas/wdiv-s3-trigger/requirements/testing.in": "cdk/lambdas/wdiv-s3-trigger/requirements/testing.txt",
    }
    for in_file, out_file in paths.items():
        if upgrade:
            msg = f"\nGenerating {out_file} from {in_file}, and looking for upgrades\n"
            cmd = f"pip-compile --generate-hashes --upgrade -o {out_file} {in_file}"
        else:
            msg = f"\nGenerating {out_file} from {in_file}, and looking for upgrades\n"
            cmd = f"pip-compile --generate-hashes -o {out_file} {in_file}"

        sys.stdout.write(msg)
        ctx.run(cmd)
