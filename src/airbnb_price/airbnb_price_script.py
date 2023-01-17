import sys
import boto3
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame, SparkSession

def airbnb_script(resource_bucket, data_bucket):
    """""
    This glue script utilizes 3 nodes and 2 buckets.
    The first bucket is our resource, where we grab the raw data.
    
    When data is grabbed from the first node, we send it to the 2nd node.

    The 2nd node transforms our data to then be sent off to the third node
    which holds the scond bucket.
    
    """""
    # Context build/setup
    spark_context = SparkContext()
    glue_context = GlueContext(spark_context)
    logger = glue_context.get_logger()
    # spark = glue_context.spark_session

    # Gives access to arguments passed into our glue script when job is ran
    args = getResolvedOptions(sys.argv, ["JOB_NAME"])
    glue_job = Job(glue_context)
    glue_job.init(args["JOB_NAME"], args) # Start job

    logger.info("Starting nguyen-airbnb-glue-job")

    # Script generated for node S3 bucket
    resource_node = glue_context.create_dynamic_frame.from_options(
        format_options = {
            "quoteChar": '"',
            "withHeader": True,
            "separator": ",",
            "optimizePerformance": False,
        },
        connection_type = "s3",
        format = "csv",
        connection_options = {
            "paths": [
                resource_bucket
            ],
            "recurse": True,
        },
        transformation_ctx = "resource_node",
    )

    # Transform data from csv to table?
    mapping_node = ApplyMapping.apply(
        frame = resource_node,
        mappings = [
            ("listing_id", "bigint", "listing_id", "long"),
            ("price", "string", "price", "string"),
            ("nbhood_full", "string", "nbhood_full", "string"),
        ],
        transformation_ctx = "mapping_node",
    )

    # Push transformed data into S3 bucket
    data_node = glue_context.getSink(
        path = data_bucket,
        connection_type = "s3",
        updateBehavior = "UPDATE_IN_DATABASE",
        partitionKeys = [],
        enableUpdateCatalog = True,
        transformation_ctx = "data_node",
    )
    data_node.setCatalogInfo(
        catalogDatabase = "nguyen-airbnb-db", catalogTableName="area-prices"
    )
    data_node.setFormat("glueparquet")
    data_node.writeFrame(mapping_node)
    
    glue_job.commit()
    logger.info("Finished job!")
    