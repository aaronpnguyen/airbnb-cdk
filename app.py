import os

import aws_cdk as cdk
from stacks.airbnb.airbnb_stack import AirbnbStack
from stacks.snowflake.snowflake_stack import SnowflakeStack

app = cdk.App()

airbnb_stack = AirbnbStack(app, "nguyen-airbnb-stack")

snowflake_stack = SnowflakeStack(app, "nguyen-snowflake-stack", data_bucket=airbnb_stack.data_bucket)

app.synth()
