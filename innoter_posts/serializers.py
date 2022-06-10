from rest_framework import serializers
from innoter_posts.models import Post


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


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'updated_at')
