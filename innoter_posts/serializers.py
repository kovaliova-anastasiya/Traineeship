from rest_framework import serializers
from innoter_posts.models import PostLike, Post
from innoter_user.serializers import ListUserSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()

    class Meta:
        model = PostLike
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    # retweets_count = serializers.SerializerMethodField()
    likes = LikeSerializer(source='postlike_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'created_at', 'updated_at', 'likes_count', 'likes')

    @staticmethod
    def get_likes_count(self):
        return self.likes.count()


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
