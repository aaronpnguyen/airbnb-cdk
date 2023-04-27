import os

import aws_cdk as cdk
from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3
)
from constructs import Construct

class SnowflakeStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, data_bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ####################################
        #         Policies & Roles         #
        ####################################

        snowflake_arn = os.environ["SNOWFLAKE_ARN"]
        snowflake_id = os.environ["SNOWFLAKE_ID"]

        # Setting up needed policies (get and list buckets) for snowflake role
        snowflake_access_policy = iam.PolicyDocument(
            statements = [
                iam.PolicyStatement(
                    actions = [
                        "s3:GetObject",
                        "s3:GetObjectVersion"
                    ],
                    resources = [
                        f"{data_bucket.bucket_arn}/*"
                    ],
                    effect = iam.Effect.ALLOW
                ),
                iam.PolicyStatement(
                    actions = [
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
                    ],
                    resources = [
                        data_bucket.bucket_arn
                    ],
                    effect = iam.Effect.ALLOW
                )
            ]
        )

        iam.Role(
            self,
            "nguyen-snowflake-access-role",
            role_name = "nguyen-snowflake-access-role",
            assumed_by = iam.ArnPrincipal(snowflake_arn), 
            external_ids = [snowflake_id],
            inline_policies = {"nguyen-snowflake-access-policies": snowflake_access_policy}
        )
        