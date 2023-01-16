#!/usr/bin/env python3
import os

import aws_cdk as cdk

from airbnb_cdk.airbnb_cdk_stack import AirbnbCdkStack


app = cdk.App()

main_stack = AirbnbCdkStack(app, "nguyen-airbnb-stack")

app.synth()
