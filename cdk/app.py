#!/usr/bin/env python3

import os

from aws_cdk import core as cdk

from stacks.wdiv_stack import WDIVStack


app = cdk.App()
WDIVStack(
    app,
    "WDIVStack",
    env=cdk.Environment(account="356853674636", region="eu-west-2"),
)

app.synth()
