from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_newpost_notification(sender, recipient):
    subject = 'New post notification'
    body = f'{sender} has published a new post!'
    send_mail(subject, body, sender, [recipient], fail_silently=False)
