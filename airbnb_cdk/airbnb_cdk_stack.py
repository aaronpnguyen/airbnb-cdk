import aws_cdk as cdk
from aws_cdk import (
    aws_athena,
    aws_cloudwatch,
    aws_cloudwatch_actions,
    aws_events,
    aws_glue,
    aws_glue_alpha,
    aws_s3,
    aws_s3_deployment,
    aws_iam as iam
)
from constructs import Construct

class AirbnbCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        

        ####################################
        #              Glue!               #
        ####################################

        self.glue_db = aws_glue_alpha.Database(
            self,
            "nguyen-airbnb-db-deployment", # Id as a string
            database_name = "nguyen-airnb-db" # Name
        )

        ####################################
        #             Buckets!             #
        ####################################

        s3_client = aws_s3.Bucket(self, "nguyen-airnb-data-bucket")

        # Deploying resources to specified bucket
        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-deployment", # Name of bucket
            sources = [ # Sources must be directories or zip files
                aws_s3_deployment.Source.asset("resources")
            ],
            destination_bucket = s3_client # Where we send the resource
        )
