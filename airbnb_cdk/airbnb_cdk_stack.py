import aws_cdk as cdk
from aws_cdk import (
    aws_glue_alpha as glue,
    aws_s3,
    aws_s3_deployment,
    aws_lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam
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

        resource_url = resource_bucket.s3_url_for_object()
        data_url = data_bucket.s3_url_for_object()

        ####################################
        #          Bucket Resources!       #
        ####################################

        # Airbnb csv data
        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-deployment", # Name of bucket
            sources = [ # Sources must be directories or zip files
                aws_s3_deployment.Source.asset("resources")
            ],
            destination_bucket = resource_bucket # Where we send the resource
        )

        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-data-deployment", # Name of bucket
            sources = [ # Sources must be directories or zip files
                aws_s3_deployment.Source.asset("transformed_data")
            ],
            destination_bucket = data_bucket # Where we send the resource
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
        #              Lambda!             #
        ####################################

        aws_lambda.Function(self, "nguyen-test-lambda",
            runtime = aws_lambda.Runtime.PYTHON_3_8,
            handler = "airbnb-lambda",
            code = aws_lambda.Code.from_asset("lambdas")
        )


        ####################################
        #              Glue!               #
        ####################################

        self.glue_db = glue.Database(
            self,
            "nguyen-airbnb-db-glue", # Id as a string
            database_name = "nguyen-airbnb-db" # Name
        )

        # For now we're assuming full access, but usually we'd want to implement
        # The least amount of access
        glue.Job(self, "nguyen-airbnb-price-job",
            executable = glue.JobExecutable.python_etl(
                glue_version = glue.GlueVersion.V3_0,
                script = glue.Code.from_bucket(glue_bucket, 'airbnb_price_script.py'),
                python_version = glue.PythonVersion.THREE,
            ),
            default_arguments = {
                "--resource_bucket": resource_url,
                "--data_bucket": data_url
            },
            description = "airbnb-etl"
        )

        """
        glue_read_actions = [
            "glue:GetConnection",
            "glue:GetDatabase",
            "glue:GetDatabases",
            "glue:GetTable",
            "glue:GetTables",
        ]

        glue_roles = iam.Role(
            self,
            "nguyen-airbnb-etl-role",
            role_name = "nguyen-airbnb-etl",
            assumed_by = iam.ServicePrincipal("glue.amazonaws.com"),
            inline_policies = {
                "glue_policy": iam.PolicyDocument(
                    statements = [
                        iam.PolicyStatement(
                            actions = [
                                *glue_read_actions,
                                "glue:CreateTable",
                                "glue:DeleteTable"
                            ],
                            resources = [self.glue_db.catalog_arn, self.glue_db.database_arn]
                        )
                    ]
                )
            }
        )
        """

        ####################################
        #            DynamoDb!             #
        ####################################

        test_table = dynamodb.Table(
            self,
            "nguyen-test-table",
            billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery = True,
            removal_policy = cdk.RemovalPolicy.DESTROY,
            time_to_live_attribute = "ttl",
            partition_key = dynamodb.Attribute(name = "id", type = dynamodb.AttributeType.STRING),
            sort_key = dynamodb.Attribute(name = "second_key", type = dynamodb.AttributeType.STRING)
        )