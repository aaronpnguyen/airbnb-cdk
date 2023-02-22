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

        # Glue scripts
        aws_s3_deployment.BucketDeployment(
            self,
            "nguyen-airbnb-glue-deployment",
            sources = [
                aws_s3_deployment.Source.asset("src/glue")
            ],
            destination_bucket = glue_bucket
        )

        s3_actions = [
            "s3:ListBucket",
            "s3:ListBuckets",
            "s3:ListAllMyBuckets",
            "s3:GetBucketLocation",
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
        ]

        s3_policy_statement = iam.PolicyStatement(
            actions = [*s3_actions],
            effect = iam.Effect.ALLOW,
            resources = [
                "*"
            ]
        )

        ####################################
        #              Lambda!             #
        ####################################

        airbnb_lambda = aws_lambda.Function(self, "airbnb_lambda",
            runtime = aws_lambda.Runtime.PYTHON_3_8,
            handler = "airbnb_lambda.main",
            code = aws_lambda.Code.from_asset("src/lambdas")
        )

        ####################################
        #              Glue!               #
        ####################################

        self.glue_db = glue.Database(
            self,
            "nguyen-airbnb-db-glue", # Id as a string
            database_name = "nguyen-airbnb-db" # Name
        )

        glue_read_actions = [
            "glue:GetConnection",
            "glue:GetDatabase",
            "glue:GetDatabases",
            "glue:GetTable",
            "glue:GetTables",
            "glue:CreateTable",
            "glue:DeleteTable",
            "glue:DeleteTable",
        ]

        glue_policy_statement = iam.PolicyStatement(
            actions = glue_read_actions,
            resources = [
                self.glue_db.catalog_arn,
                self.glue_db.database_arn
            ],
            effect = iam.Effect.ALLOW
        )

        glue_role = iam.Role(
            self,
            "nguyen-airbnb-etl-role",
            role_name = "nguyen-airbnb-etl",
            assumed_by = iam.ServicePrincipal("glue.amazonaws.com"),
            inline_policies = {
                "glue_policy": iam.PolicyDocument(
                    statements = [
                        glue_policy_statement,
                        s3_policy_statement
                    ]
                )
            }
        )
        
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
            role = glue_role,
            description = "airbnb-etl"
        )
        
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
        )

        test_table.grant_read_write_data(airbnb_lambda.role)

        ####################################
        #            Policies!             #
        ####################################

        iam.ManagedPolicy(
            self,
            "nguyen-airbnb-managed-policy",
            document = iam.PolicyDocument(
                statements=[
                    glue_policy_statement,
                    s3_policy_statement,
                ]
            )
        )