# wdiv-s3-trigger


# TODO: UPDATE ALL OF THIS

Install uv

Create cdk/lambdas/wdiv-s3-trigger/requirements.txt:
```
./cdk/scripts/wdiv-s3-trigger-requirements.sh
```

Deploy with:
```
cdk  --profile dev-wdiv-dc --context dc-environment=development deploy WDIVS3TriggerStack
```



[![Build Status](https://travis-ci.org/DemocracyClub/wdiv-s3-trigger.svg?branch=master)](https://travis-ci.org/DemocracyClub/wdiv-s3-trigger)
[![Coverage Status](https://coveralls.io/repos/github/DemocracyClub/wdiv-s3-trigger/badge.svg?branch=master)](https://coveralls.io/github/DemocracyClub/wdiv-s3-trigger?branch=master)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)


## About

This project defines a lambda function which is triggered when a new file is written to `TEMP_BUCKET_NAME` and performs the following high-level tasks:

* Perform some checks on the file(s) and generate a report
* If all the checks pass:
  * Raise a Github issue
  * Copy the input files from `TEMP_BUCKET_NAME` to `FINAL_BUCKET_NAME`
  * Write a copy of the report to `FINAL_BUCKET_NAME`
* If any checks fail:
  * Send someone an email
* Report the result back to an API endpoint on wheredoivote

The [corresponding application code in wheredoivote](https://github.com/DemocracyClub/UK-Polling-Stations/tree/master/polling_stations/apps/file_uploads) allows users to upload files to `TEMP_BUCKET_NAME` and defines the API endpoint which receives the report.

The main thing this project does is interact with a number of external services and APIs, namely:

* Amazon S3
* Amazon SES
* GitHub
* wheredoivote

When you strip all those interactions away, there isn't much left. As such:

* You can use TDD to develop locally, but it requires some fiddly setup to mock out all the interactions with external services. Fortunately there are some [integration tests](https://github.com/DemocracyClub/wdiv-s3-trigger/blob/master/tests/test_handler.py) which use [moto](https://github.com/spulec/moto) and [responses](https://github.com/getsentry/responses) for mocking which can serve as a pattern for future development.
* In order to manually trigger the function, it is easiest to deploy to a staging lambda with staging buckets configured. SLS manages bucket permissions for the lambda function itself, but local/staging/live deploys of the WDIV codebase need to be able to write to the bucket defined in `TEMP_BUCKET_NAME`. This may be configured using tokens or role-based auth.
* It is important to deploy with an appropriate [configuration](#configuration), and conversely, there is potential to make a mess in the real world/live environment by deploying with an incorrect configuration (e.g: staging deploy with real keys).

## Local Development

* Install Python dependencies: `pipenv install --dev`
* Install Node JS dependencies: `npm install`
* Run the test suite: `./run_tests.py`
* Sort imports: `isort **/*.py`
* Run lint checks: `flake8 .`
* Auto-format: `black .`

## Configuration

```sh
cp settings.dev.template.json settings.dev.json
cp settings.prod.template.json settings.prod.json
```

* `TEMP_BUCKET_NAME`
  * Required
  * The S3 bucket to pick uploaded files from. This is the bucket the trigger is registered on. WDIV must be able to write to this bucket.
* `FINAL_BUCKET_NAME`
  * Required
  * The S3 bucket to copy files to if all the checks pass.
* `SENTRY_DSN`
  * Optional
  * If set, exceptions will be logged here.
* `GITHUB_REPO`
  * Required
  * Github repo to raise issues on.
* `GITHUB_API_KEY`
  * Optional
  * A Github API token. This tokem must have permission to raise an issue on the target repo defined in `GITHUB_REPO`.
  * If set, running the lambda action will raise an issue on the target repo if all the checks pass.
  * If not set, running the lambda action will log the details of the issue that would be raised to the CloudWatch logs.
  * In most cases, `GITHUB_API_KEY` should not be set for test/dev deploys.
* `WDIV_WEBHOOK_URL`
  * Required
  * URL of an endpoint on wheredoivote.co.uk (or stage.wheredoivote.co.uk ) to `POST` back to after the lambda runs.
* `WDIV_API_KEY`
  * Optional
  * A wheredoivote API token. This token must belong to a user with the `is_superuser` flag.
  * If set, running the lambda action will post a response back to the endpoint defined in `WDIV_API_KEY`.
  * If not set, running the lambda action will log the details of the response that would have been sent to the CloudWatch logs.
  * In most cases, `WDIV_API_KEY` should not be set for test/dev deploys.
* `ERROR_REPORT_EMAIL`
  * Optional
  * An email address to notify when checks are failed.
  * If set, running the lambda action will send an email to `ERROR_REPORT_EMAIL` when a file with errors is detected.
  * In most cases, `ERROR_REPORT_EMAIL` should not be set for test/dev deploys.

## Deployment

* `AWS_PROFILE=wheredoivote npm run deploy:dev` (use settings from `settings.dev.json`)
* `AWS_PROFILE=wheredoivote npm run deploy:prod` (use settings from `settings.prod.json`)
