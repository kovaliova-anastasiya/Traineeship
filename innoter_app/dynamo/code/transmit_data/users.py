import boto3
from innoter_user.models import User

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Users')


def create_user_record(user):
    table.put_item(
        Item={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'image_s3_path': user.image_s3_path,
            'u_role': user.role,
            'title': user.title,
            'is_blocked': user.is_blocked,
        }
    )


def update_user_record(user):
    table.update_item(
        Key={
            'username': user.username,
        },
        UpdateExpression="set first_name = :first_name, \
                        last_name = :last_name, \
                        email = :email, \
                        image_s3_path = :image_s3_path, \
                        u_role = :u_role, \
                        title = :title, \
                        is_blocked = :is_blocked",
        ExpressionAttributeValues={
            ':first_name': user.first_name,
            ':last_name': user.last_name,
            ':email': user.email,
            ':image_s3_path': user.image_s3_path,
            ':u_role': user.role,
            ':title': user.title,
            ':is_blocked': user.is_blocked,
        },
    )


def delete_user_record(user):
    table.delete_item(
        Key={
            'username': user.username,
        }
    )
