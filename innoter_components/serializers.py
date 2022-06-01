from rest_framework import serializers
from innoter_components.models import Tag, Page, Post


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TagRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


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


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'created_at', 'updated_at')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'created_at', 'updated_at')


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'updated_at')
