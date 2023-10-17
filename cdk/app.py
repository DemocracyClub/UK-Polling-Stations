#!/usr/bin/env python3

import os

from aws_cdk import App, Environment, Tags
from stacks.command_runner_stack import WDIVOncePerTagCommandRunner
from stacks.wdiv_s3_trigger_stack import WDIVS3TriggerStack
from stacks.wdiv_stack import WDIVStack

valid_environments = (
    "development",
    "staging",
    "production",
)

app_wide_context = {}
if dc_env := os.environ.get("DC_ENVIRONMENT"):
    app_wide_context["dc-environment"] = dc_env

app = App(context=app_wide_context)

env = Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="eu-west-2")

# Set the DC Environment early on. This is important to be able to conditionally
# change the stack configurations
dc_environment = app.node.try_get_context("dc-environment") or None
assert (
    dc_environment in valid_environments
), f"context `dc-environment` must be one of {valid_environments}"


WDIVStack(
    app,
    "WDIVStack",
    env=env,
)

WDIVS3TriggerStack(app, "WDIVS3TriggerStack", env=env)

WDIVOncePerTagCommandRunner(app, "WDIVOncePerTagCommandRunner", env=env)

Tags.of(app).add("dc-product", "wdiv")
Tags.of(app).add("dc-environment", dc_environment)

app.synth()
