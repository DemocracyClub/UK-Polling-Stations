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

## Create a deployment group
AWS_PROFILE=dev-wdiv-dc DC_ENVIRONMENT=development python deploy/create_deployment_group.py
