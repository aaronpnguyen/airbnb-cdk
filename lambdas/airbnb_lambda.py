import boto3

def main(event, context):
    dynamo_client = boto3.resource('dynamodb')

    table = dynamo_client.table('airbnb-ddb')

    item = {
        "item.name": "item.value"
    }

    response = table.put_item(item)
    return item

if __name__ == "__main__":
    # Testing purposes?
    main(None, None)
