from fastapi import FastAPI
from code.db import initialize_db
from boto3.dynamodb.conditions import Key, Attr
import boto3


app = FastAPI()

dynamodb = initialize_db()

users_table = dynamodb.Table('Users')
pages_table = dynamodb.Table('Pages')
posts_table = dynamodb.Table('Posts')


@app.get('/')
def index():
    return {"message": "hello world"}


@app.get('/this_user/{username}')
def get_user_info(username: str):
    response = users_table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    items = response['Items']
    print(items)
    return items


@app.get('/count/{username}/pages')
def count_user_pages(username: str):
    response = pages_table.scan(
        FilterExpression=Attr('owner').eq(username)
    )
    items = response['Items']
    return {f'User "{username}" has {len(items)} pages'}


@app.get('/count/{username}/posts')
def count_user_posts(username: str):
    response = posts_table.scan(
        FilterExpression=Attr('post_owner').eq(username)
    )
    items = response['Items']
    return {f'User "{username}" has {len(items)} posts'}


@app.get('/mean/foll/{username}')
def mean_followers_per_page(username: str):
    response = pages_table.scan(
        FilterExpression=Attr('owner').eq(username)
    )
    pages = response['Items']

    overall_followers_amount = 0
    for i in range(0, len(pages)):
        page_followers_amount = len(pages[i]['followers'])
        overall_followers_amount += page_followers_amount

    try:
        mean_followers_per_page = round(overall_followers_amount/len(pages), 3)
        return f'The mean amount of "{username}" followers per page is {mean_followers_per_page}'
    except:
        return f'The mean amount of "{username}" followers per page is 0'


@app.get('/mean/likes/{username}')
def mean_likes_per_post(username: str):
    response = posts_table.scan(
        FilterExpression=Attr('post_owner').eq(username)
    )
    posts = response['Items']

    overall_likes_amount = 0
    for i in range(0, len(posts)):
        post_likes_amount = len(posts[i]['likes'])
        overall_likes_amount += post_likes_amount
    try:
        mean_likes_per_page = round(overall_likes_amount / len(posts), 3)
        return f'The mean amount of "{username}" followers per page is {mean_likes_per_page}'
    except:
        return f'The mean amount of "{username}" followers per page is 0'

