import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

def main():
    """""
    This glue script utilizes 3 nodes and 2 buckets.
    The first bucket is our resource, where we grab the raw data.
    
    When data is grabbed from the first node, we send it to the 2nd node.

    The 2nd node transforms our data to then be sent off to the third node
    which holds the scond bucket.
    
    """""

    # Temp var
    resource_bucket = "s3://nguyen-airbnb-stack-nguyenairbnbresourcebucket398-7r28e7ydn9g0"
    data_bucket = "s3://nguyen-airbnb-stack-nguyenairbnbdatabucket5f319e0-8a4lg64btd1a"

    # Context build/setup
    spark_context = SparkContext()
    logger = GlueContext(spark_context).get_logger()
    glue_context = GlueContext(spark_context.getOrCreate())

    logger.info("Starting job!")

    raw_dataframe = glue_context.create_dynamic_frame_from_options(
        connection_type="s3",
        connection_options={"paths": [resource_bucket]},
        format="csv",
        format_options={
            "withHeader": True
        }
    )

    glue_context.write_dynamic_frame_from_options(
        frame = raw_dataframe,
        connection_type = "s3",
        connection_options={"paths": [data_bucket]},
        format = "parquet"
    )

    logger.info("Finshed job!")

if __name__ == "__main__":
    main()