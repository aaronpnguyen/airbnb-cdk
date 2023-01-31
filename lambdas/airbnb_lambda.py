import logging
import os
import boto3

logger = logging.getLogger(__name__)
logger.setLevel

def main(event, context):
    dynamo_client = boto3.resource('dynamodb')

    table = dynamo_client.Table('nguyen-airbnb-stack-nguyentesttable3D24C418-DRTHK70VG0I1')

    response = table.put_item(
        Item = {
            "id": "1",
            "status_code": "200",
            "second_key": "useful?"
        }
    )
    return response

if __name__ == "__main__":
    # Testing purposes?
    main(None, None)
