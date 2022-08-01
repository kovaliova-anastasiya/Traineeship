import boto3
from innoter_posts.models import Post


dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Posts')


def create_post_record(post):
    table.put_item(
        Item={
            'page': post.page.name,
            'pk': post.pk,
            'content': post.content,
            'reply_to': post.reply_to,
            'post_owner': post.page.owner.username,
            'likes': list(user.username for user in post.likes.all()),
            'created_at': str(post.created_at),
            'updated_at': str(post.updated_at),
        }
    )


def update_post_record(post):
    table.update_item(
        Key={
            'page': post.page.name,
            'pk': post.pk
        },
        UpdateExpression="set content = :content, \
                        reply_to = :reply_to, \
                        post_owner = :post_owner, \
                        likes = :likes, \
                        updated_at = :updated_at",
        ExpressionAttributeValues={
            ':content': post.content,
            ':reply_to': post.reply_to,
            ':post_owner': post.page.owner.username,
            ':likes': list(user.username for user in post.likes.all()),
            ':updated_at': str(post.updated_at),
        },
    )


def delete_post_record(post):
    table.delete_item(
        Key={
            'page': post.page.name,
            'pk': post.pk
        }
    )

