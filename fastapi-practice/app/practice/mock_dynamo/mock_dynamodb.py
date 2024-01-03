import boto3
from moto import mock_dynamodb


def write_into_table(item, table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        batch.put_item(Item=item)


def create_and_write_into_table(data_set, table_name):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(TableName=table_name,
                                  KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                                  AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
                                  BillingMode="PAY_PER_REQUEST")
    for data in data_set:
        write_into_table(data, table_name)

    ### Your code will be here

    return ""


@mock_dynamodb
def dynamo_db_function_name(): #Create one method for every type of operation you need from DYNAMODB
    pass