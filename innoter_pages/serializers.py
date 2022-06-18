from rest_framework import serializers
from innoter_pages.models import Page
from innoter_user.models import User
from innoter_user.serializers import ListUserSerializer


class PageSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    # followers = ListUserSerializer(many=True)

    class Meta:
        model = Page
        fields = ('followers', 'follow_requests', 'followers_count', 'unblock_date',
                  'tags')

    @staticmethod
    def get_followers_count(self):
        return self.followers.count()


class ShowTagsAttachedSerializer(serializers.ModelSerializer):
        class Meta:
            model = Page
            fields = ('pk', 'tags')


class ShowFollowersSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followers = ListUserSerializer(many=True)

    class Meta:
        model = Page
        fields = ('followers_count', 'followers')

    @staticmethod
    def get_followers_count(self):
        return self.followers.count()


class ShowRequestsSerializer(serializers.ModelSerializer):
    follow_requests_count = serializers.SerializerMethodField()
    follow_requests = ListUserSerializer(many=True)

    class Meta:
        model = Page
        fields = ('follow_requests_count', 'follow_requests')

    @staticmethod
    def get_follow_requests_count(self):
        return self.follow_requests.count()


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