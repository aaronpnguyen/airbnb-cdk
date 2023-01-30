import boto3

def lambda_handler(event, context):
    dynamo_client = boto3.resource('dynamodb')

    table = dynamo_client.table('airbnb-ddb')

    item = {
        "item.name": "item.value"
    }

    response = table.put_item(item)
    return item
