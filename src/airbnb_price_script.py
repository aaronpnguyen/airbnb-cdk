import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# This is passed in through "--default_arguments" in stack file
args = getResolvedOptions(sys.argv, 
    [
        "JOB_NAME",
        "resource_bucket",
        "data_bucket"
    ]
)

job_name = args["JOB_NAME"]
resource_bucket = args["resource_bucket"]
data_bucket = args["data_bucket"]

spark_context = SparkContext()
glueContext = GlueContext(spark_context)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(job_name, args)

# Identify resource bucket and file type
resource_node = glueContext.create_dynamic_frame.from_options(
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

# Write transformed data into correct file type/format
output_node = glueContext.getSink(
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

# Finishing job
job.commit()
