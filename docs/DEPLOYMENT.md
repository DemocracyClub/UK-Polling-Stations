# Deployment

## Overview

There are three AWS accounts `dev`, `staging` and `production`. New features can be trialled in `dev`.
The `staging` environment is a test for deployments before being deployed to `production`.
In general deployments to `staging` and `production` will be triggered when a PR is merged, and happen in CircleCI.

## CDK vs Codedeploy

CDK is used to create and define the aws resources to serve the app.
Codedeploy is responsible for taking an instance as defined in the `LaunchTemplate` (defined as part of the `WDIVStack`)
and installing the application on it.


## AWS Resources
[AWS Resources diagram](./aws-resources.png)

## SSO cli
```shell
aws sso login --profile dev-wdiv-dc
```

## Working with CDK

```Shell
cdk deploy --all --context dc-environment=development --profile dev-wdiv-dc
```


## WDIV-s3-trigger

```
cdk  --profile dev-wdiv-dc --context dc-environment=development deploy WDIVS3TriggerStack
```

When setting up a new circleci environment, make sure to provide the following environment variables as part of a context:

  - `FINAL_BUCKET_NAME`
  - `SENTRY_DSN`
  - `GITHUB_REPO`
  - `GITHUB_API_KEY`
  - `WDIV_API_KEY`
  - `ERROR_REPORT_EMAIL`
  - `WDIV_WEBHOOK_URL`


## Working with CodeDeploy

### Kicking off deploys from local machine
Use the `create_deployment.py` script.
It expects the `COMMIT_SHA` environment variable to be set, and will also look for relevant AWS environment credentials.

e.g.
```shell
AWS_PROFILE=dev-wdiv-dc COMMIT_SHA=`git rev-parse HEAD` python deploy/create_deployment.py
```

### [codedeploy-local](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-local.html)
When modifying `appspec.yml` and it's various scripts you can get a fairly tight cycle with `codedeploy-local`.
This involves running a deploy against the machine you're on. This is best done on an EC2 instance, the call to `codedeploy-local` will then modify that instance, allowing one to debug it when there are failures.
The following steps outline the general workflow:

- Launch an EC2 instance from your `LaunchTemplate` (this should have CodeDeployAgent already installed).
- Connect to the instance (eg `mssh --profile dev-wdiv-dc -r eu-west-2 -X "ubuntu@i-12345a67b8cd9ef0"`)
- Then you can either run a deploy from github:
```shell
sudo /opt/codedeploy-agent/bin/codedeploy-local \
  --bundle-location https://api.github.com/repos/DemocracyClub/{REPONAME}/tarball/{BRANCHNAME|COMMIT} \
  --type tar
```
- Or clone the repo to the instance, checkout the relevant branch, and run:
```shell
sudo /opt/codedeploy-agent/bin/codedeploy-local \
  --bundle-location path/to/repo/ \
  --type directory
```

If you've followed the latter option then you are able to make changes to the cloned repo, and re-run the script.
If one hook has run successfully (eg `BeforeInstall`) you can focus on a single hook:
```shell
sudo /opt/codedeploy-agent/bin/codedeploy-local \
  --bundle-location path/to/repo/ \
  --type directory
  --events AfterInstall
```

# Setting up a new environment


Assuming you can authenticate against the account locally. If you're using
AWS SSO then this means passing `--profile [env]-ee-dc` to CDK and other AWS CLI commands.

### Create an RDS Instance
Create a security group called `rds-public-access`. Set a single inbound rule of type `PostgreSQL` and excepting traffic from anywhere.
Do this in the console. Make sure the Postgres version you select matches the version used in the base image. eg pg14.4 is default available on 22.04 at time of writing
Assign the security group.

Create a db
```
$ psql postgresql://postgres@pollingstations.chxtxn9vr5tl.eu-west-2.rds.amazonaws.com
postgres=> create database polling_stations;
postgres=> \q
```

Create postgis extension
```
$ psql postgresql://postgres@pollingstations.chxtxn9vr5tl.eu-west-2.rds.amazonaws.com/polling_stations
polling_stations=> create extension postgis;
polling_stations=> \q
```

Do a restore of db schema only

```
$ pg_restore \
    -U postgres \
    -h  pollingstations.chxtxn9vr5tl.eu-west-2.rds.amazonaws.com \
    -p 5432 \
    -c \
    -j 2 \
    --if-exists \
    --no-owner \
    --no-privileges \
    --role=postgres \
    -d polling_stations \
    ~/Downloads/polling_stations_schema.dump

```

Set up Replication

```
polling_stations=> CREATE PUBLICATION alltables FOR ALL TABLES;
```

Create Parameter group and apply it. Use `cdk/scripts/create_logical_parameter_group.py`
eg
`AWS_PROFILE=prod-wdiv-dc DB_IDENTIFIER=pollingstations python cdk/scripts/create_logical_parameter_group.py`

### 1 AWS Deployment user

We need a user that can deploy the application.

Because CDK uses CloudFormation to do a lot, it's recommended that the deployment user has administrative
access. This is typically a bad idea, but it's very hard to get CloudFormation working without it.

1. Create an IAM user called `CircleCIDeployer` in the AWS console
2. Select `Programmatic access`
3. Attach the existing `AdministratorAccess` policy
4. Continue and download the CSV with the access keys

Create a circleCI context with the appropriate values.

### 2 Domain name and TLS certificate

#### DNS
1. Make a new hosted zone in the target account
2. Delegate the NS of the intended domain to the hosted zone's name servers

#### Cert
Once the Domain nam is set up, use AWS Certificate Manager to create a cert.

NOTE: This MUST be in the `us-east-1` account to work with CloudFront. You will have to delete and re-create
the cert if you make it in the wrong region.

### 3 Create an RDS instance

### 3 AWS Parameter Store

The CDK Stack requires some parameters that are taken from the SSM Parameter Store:

* `FQDN`: the domain name you assigned above that you want to app to be serverd from
* `SSL_CERTIFICATE_ARN`: the ARN of the ACM cert you made above
* `OrganisationID` the ID of the AWS organisation this is sitting in. Used for Image Builder to share AMIs

### 4 Bootstrap CDK

```shell

cdk bootstrap --profile=[dev|stage|prod]-wdiv-dc --context dc-environment=[development|staging|production]
```

CDK will create various AWS resources that are needed to deploy the stacks. This includes
an S3 bucket and some IAM roles.

See [CDK bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html) for more.


### CDK Deploy

### Code deploy

Create a deployment group
```
AWS_PROFILE=prod-wdiv-dc DC_ENVIRONMENT=production python deploy/create_deployment_group.py
```

create a deployment
```
AWS_PROFILE=prod-wdiv-dc DC_ENVIRONMENT=production COMMIT_SHA=`git rev-parse HEAD`  python deploy/create_deployment.py
```
That will spin up an instance, grab it's id and SH in and kick off a deploy
```
local$ mssh --profile prod-wdiv-dc -r eu-west-2 -X "ubuntu@i-024f88a726d07383f"

instance$ sudo /opt/codedeploy-agent/bin/codedeploy-local \
  --bundle-location https://api.github.com/repos/DemocracyClub/UK-Polling-Stations/tarball/cdk \
  --type tar
```

## Create a deployment group
AWS_PROFILE=dev-wdiv-dc DC_ENVIRONMENT=development python deploy/create_deployment_group.py

#### Trouble shooting

* "The deployment failed because no instances were found in your blue fleet"
  * Edit `Environment configuration` in the deployment Group, select the asg which contains instancs you wish to replace.
