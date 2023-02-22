import logging
import os
import boto3

logger = logging.getLogger(__name__)
logger.setLevel

def main(event, context):
    table_name = os.environ["DYNAMODB_TABLE"]
    dynamo_resource = boto3.resource('dynamodb')

    table = dynamo_resource.Table(table_name)

    dynamodb_content = table.scan()

    response = table.put_item(
        Item = {
            "id": f"{dynamodb_content['Count'] + 1}",
            "description": "Lambda deployed!"
        }
    )

    return response

if __name__ == "__main__":
    main(None, None)
