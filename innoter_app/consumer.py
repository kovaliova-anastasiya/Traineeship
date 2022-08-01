import json
import pika
import django
from sys import path
from os import environ

path.append('/innoter/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'innoter.settings')
django.setup()

from dynamo.code.transmit_data.posts import create_post_record, \
    update_post_record, delete_post_record
from dynamo.code.transmit_data.pages import create_page_record, \
    update_page_record, delete_page_record
from dynamo.code.transmit_data.users import create_user_record, \
    update_user_record, delete_user_record
from dynamo.code.generate_tables.pages import generate_pages_table
from dynamo.code.generate_tables.posts import generate_posts_table
from dynamo.code.generate_tables.users import generate_users_table
from dynamo.code.db import initialize_db
from innoter_posts.models import Post
from innoter_pages.models import Page
from innoter_user.models import User


connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq', heartbeat=600,
                              blocked_connection_timeout=300))

channel = connection.channel()
channel.queue_declare(queue='db')

print('there')


def callback(ch, method, properties, body=''):
    print("Received in db_consumer")

    pk = json.loads(body)
    dynamodb = initialize_db()

    try:
        if properties.content_type == 'create_table_pages':
            generate_pages_table(dynamodb)
            print('pages table created')

        elif properties.content_type == 'create_table_posts':
            generate_posts_table(dynamodb)
            print('posts table created')

        elif properties.content_type == 'create_table_users':
            generate_users_table(dynamodb)
            print('users table created')

        elif properties.content_type == 'transmit_pages':
            for page in Page.objects.all():
                try:
                    update_page_record(page)
                except:
                    create_page_record(page)
            print("pages data transmitted")

        elif properties.content_type == 'transmit_posts':
            for page in Post.objects.all():
                try:
                    update_post_record(page)
                except:
                    create_post_record(page)
            print("posts data transmitted")

        elif properties.content_type == 'transmit_users':
            for user in User.objects.all():
                try:
                    update_user_record(user)
                except:
                    create_user_record(user)
            print("users data transmitted")

        elif properties.content_type == 'create_post':
            create_post_record(Post.objects.get(pk=pk))
            print("post record created")

        elif properties.content_type == 'update_post':
            update_post_record(Post.objects.get(pk=pk))
            print("post record updated")

        elif properties.content_type == 'delete_post':
            delete_post_record(Post.objects.get(pk=pk))
            print("post record deleted")

        elif properties.content_type == 'create_page':
            create_page_record(Page.objects.get(pk=pk))
            print('page record created')

        elif properties.content_type == 'update_page':
            update_page_record(Page.objects.get(pk=pk))
            print('page record updated')

        elif properties.content_type == 'update_page':
            delete_page_record(Page.objects.get(pk=pk))
            print('page record deleted')

        elif properties.content_type == 'create_user':
            create_user_record(User.objects.get(pk=pk))
            print('user record created')

        elif properties.content_type == 'update_user':
            create_user_record(User.objects.get(pk=pk))
            print('user record updated')

        elif properties.content_type == 'delete_user':
            delete_user_record(User.objects.get(pk=pk))
            print('user record deleted')
    except:
        print('consumer stuck')


channel.basic_consume(queue='db', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()
