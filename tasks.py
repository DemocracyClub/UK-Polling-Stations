import os
import subprocess
import sys

from invoke import task
import boto3


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
