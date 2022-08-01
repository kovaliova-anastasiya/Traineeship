import boto3


def generate_users_table(db):
    table_name = 'Users'
    current_table = db.Table(table_name)
    tables = list(db.tables.all())

    if current_table not in tables:
        response = db.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return response
