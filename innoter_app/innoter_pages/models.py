from django.db import models
from uuid import uuid4


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=50, unique=True, default=uuid4())
    description = models.TextField()
    tags = models.ManyToManyField('innoter_tags.Tag', related_name='page', blank=True)

    owner = models.ForeignKey('innoter_user.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('innoter_user.User', related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('innoter_user.User', related_name='requests')
    unblock_date = models.DateTimeField(null=True, blank=True)
