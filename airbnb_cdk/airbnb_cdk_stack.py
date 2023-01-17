import aws_cdk as cdk
from aws_cdk import (
    aws_glue,
    aws_glue_alpha as glue,
    aws_s3,
    aws_s3_deployment,
)
from constructs import Construct

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
        glue_bucket = aws_s3.Bucket(self, "nguyen-airbnb-glue-bucket")

        # Deploying resources to specified bucket(s)

        # Airbnb csv data
        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-deployment", # Name of bucket
            sources = [ # Sources must be directories or zip files
                aws_s3_deployment.Source.asset("resources")
            ],
            destination_bucket = resource_bucket # Where we send the resource
        )

        # Glue scripts
        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-glue-deployment",
            sources = [
                aws_s3_deployment.Source.asset("src")
            ],
            destination_bucket = glue_bucket
        )

        ####################################
        #             Resources!           #
        ####################################

        glue.Job(self, "nguyen-airbnb-price-job",
            executable = glue.JobExecutable.python_etl(
                glue_version = glue.GlueVersion.V3_0,
                script = glue.Code.from_bucket(glue_bucket, 'airbnb_price_script.py'),
                python_version = glue.PythonVersion.THREE,
            ),
            description = "etl? shell? CDK testing"
        )

        # aws_glue.CfnJob(
        #     scope,
        #     "nguyen-airbnb-job",
        #     name = "nguyen-airbnb-job",
        #     command = aws_glue.CfnJob.JobCommandProperty(
        #         name = "glueetl",
        #         script_location = f"s3://{glue_bucket}/airbnb_price_script.py"
        #     ),
        #     glue_version = "3.0"
        # )

        ####################################
        #              Glue!               #
        ####################################

        self.glue_db = glue.Database(
            self,
            "nguyen-airbnb-db-glue", # Id as a string
            database_name = "nguyen-airbnb-db" # Name
        )
