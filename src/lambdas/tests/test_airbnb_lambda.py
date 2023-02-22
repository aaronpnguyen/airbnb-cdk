import os

from mock import patch
from airbnb_lambda import main

def create_test_item(table):
    item = {
        "id": table['Count'],
        "description": "Lambda deployed!"
    }

    return item

@patch.dict(os.environ, {"DYNAMODB_TABLE": "table_name"})
@patch("airbnb_lambda.boto3")
def test_main(boto_mock):

    resource_mock = boto_mock.resource()
    table_mock = resource_mock.Table.return_value

    main(None, None)

    resource_mock.Table.assert_called_with("table_name")


@patch.dict(os.environ, {"DYNAMODB_TABLE": "table_name"})
@patch("airbnb_lambda.boto3")
def test_main_put_called(boto_mock):

    resource_mock = boto_mock.resource()
    table_mock = resource_mock.Table.return_value

    main(None, None)

    table_mock.put_item.assert_called()


@patch("airbnb_lambda.boto3")
def test_main_count_increased(boto_mock):

    resource_mock = boto_mock.resource()
    table_mock = resource_mock.Table.return_value
    resource_mock.Table().scan.return_value = {
        "Count": "1"
    }

    main(None, None)

    expected_item = {
        "id": "2",
        "description": "Lambda deployed!"
    }

    table_mock.put_item.assert_called_with(Item = expected_item)

