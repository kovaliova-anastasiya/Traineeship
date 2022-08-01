import boto3


def generate_posts_table(db):
    table_name = 'Posts'
    current_table = db.Table(table_name)
    tables = list(db.tables.all())

    if current_table not in tables:
        response = db.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'page',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'pk',
                    'AttributeType': 'N'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'page',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'pk',
                    'KeyType': 'RANGE'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return response
