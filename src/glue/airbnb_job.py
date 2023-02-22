import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

job_args = getResolvedOptions(sys.argv, 
    [
        "JOB_NAME",
        "resource_bucket",
        "data_bucket"
    ]
)

job_name = job_args["JOB_NAME"]
resource_bucket = job_args["resource_bucket"]
data_bucket = job_args["data_bucket"]

spark_context = SparkContext()
glue_context = GlueContext(spark_context)
spark = glue_context.spark_session
logger = glue_context.get_logger()


job = Job(glue_context)
job.init(job_name, job_args)

logger.info("Creating tables")
# Identify resource bucket and file type
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
            f"{resource_bucket}/airbnb_price.csv" # Specify the file(s) it needs to grab
        ],
        "recurse": True,
    },
    transformation_ctx = "resource_node",
)

logger.info("Mapping tables")
# Based off of file type, list headers
# (would probably want to find a way to automate this)
transformation_node = ApplyMapping.apply(
    frame = resource_node,
    mappings = [
        ("listing_id", "string", "listing_id", "string"),
        ("price", "string", "price", "string"),
        ("nbhood_full", "string", "nbhood_full", "string"),
    ],
    transformation_ctx = "transformation_node",
)

logger.info("Finding output node")
# Write transformed data into correct file type/format
output_node = glue_context.getSink(
    path = data_bucket,
    connection_type = "s3",
    updateBehavior = "LOG",
    partitionKeys = [],
    enableUpdateCatalog = True,
    transformation_ctx = "output_node",
)

# Setting Glue catalog/database name
output_node.setCatalogInfo(
    catalogDatabase="nguyen-airbnb-db", catalogTableName="airbnb-prices"
)
output_node.setFormat("glueparquet")
output_node.writeFrame(transformation_node)

logger.info("finished job")
# Finishing job
job.commit()
