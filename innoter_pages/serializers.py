from rest_framework import serializers
from innoter_pages.models import Page


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags',
                  'owner', 'followers', 'image', 'is_private',
                  'follow_requests', 'unblock_date')


class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags',
                  'owner', 'followers', 'image', 'is_private',
                  'follow_requests', 'unblock_date')


class PageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags',
                  'owner', 'followers', 'image', 'is_private',
                  'follow_requests', 'unblock_date')


class PageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags',
                  'owner', 'followers', 'image', 'is_private',
                  'follow_requests', 'unblock_date')