import boto3
from innoter_pages.models import Page


dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Pages')


def create_page_record(page):
    table.put_item(
        Item={
            'p_name': page.name,
            'uuid': page.uuid,
            'description': page.description,
            'tags': list(tag.name for tag in page.tags.all()),
            'p_owner': page.owner.username,
            'followers': list(user.username for user in page.followers.all()),
            'image': page.image,
            'is_private': page.is_private,
            'follow_requests': list(user.username for user in page.follow_requests.all()),
            'unblock_date': str(page.unblock_date),
        }
    )


def update_page_record(page):
    table.update_item(
        Key={
            'uuid': page.uuid
        },

        UpdateExpression='set p_name = :p_name, \
                            description = :description, \
                            tags = :tags, \
                            p_owner = :p_owner, \
                            followers = :followers, \
                            image = :image, \
                            is_private = :is_private, \
                            follow_requests = :follow_requests, \
                            unblock_date = :unblock_date',

        ExpressionAttributeValues={
            ':p_name': page.name,
            ':description': page.description,
            ':tags': list(tag.name for tag in page.tags.all()),
            ':p_owner': page.owner.username,
            ':followers': list(user.username for user in page.followers.all()),
            ':image': page.image,
            ':is_private': page.is_private,
            ':follow_requests': list(user.username for user in page.follow_requests.all()),
            ':unblock_date': str(page.unblock_date),
        },
    )


def delete_page_record(page):
    table.delete_item(
        Key={
            'uuid': page.uuid
        }
    )
