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
from src.airbnb_price.airbnb_price_script import airbnb_script

class AirbnbCdkStack(cdk.Stack):
    # Self refers to this specific stack!
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ####################################
        #             Buckets!             #
        ####################################

        # Deploying buckets that will contain either resources or transformed data
        resource_bucket = aws_s3.Bucket(self, "nguyen-airbnb-resource-bucket")
        data_bucket = aws_s3.Bucket(self, "nguyen-airbnb-data-bucket")

        # Deploying resources to specified bucket(s)
        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-deployment", # Name of bucket
            sources = [ # Sources must be directories or zip files
                aws_s3_deployment.Source.asset("resources")
            ],
            destination_bucket = resource_bucket # Where we send the resource
        )

        ####################################
        #              Glue!               #
        ####################################

        self.glue_db = aws_glue_alpha.Database(
            self,
            "nguyen-airbnb-db-glue", # Id as a string
            database_name = "nguyen-airbnb-db" # Name
        )
