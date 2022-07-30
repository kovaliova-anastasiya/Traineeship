import json
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from innoter_user.permissions import UserIsOwner
from innoter_pages.models import Page
from innoter_posts.models import Post
from innoter_posts.serializers import PostCreateSerializer, PostUpdateSerializer, \
    PostRetrieveSerializer, PostSerializer
from innoter_posts.like_action import LikeActionSerializer
from rest_framework.response import Response
from innoter_posts import tasks
from dynamo.code.transmit_data import posts
import boto3
from producer import publish


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # serializer_class = PostListSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all(self, request, *args, **kwargs):
        serializer = PostSerializer(self.queryset, many=True)
        tasks.celery_check.delay()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def info(self, request, *args, **kwargs):
        current_post = self.get_object()
        serializer = PostRetrieveSerializer(current_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_new(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        page_pk = request.data.get('page')
        page = Page.objects.get(pk=page_pk)
        if page.owner.pk == request.user.id:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            publish("create_post", serializer.data['pk'])

            # print(page.followers.all())
            for user in page.followers.all():
                tasks.send_newpost_notification.delay(page.owner.email, user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Impossible to alter a foreign page'},
                            status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def upd(self, request, *args, **kwargs):
        current_post = self.get_object()
        serializer = PostUpdateSerializer(instance=current_post, data=request.data, partial=True)
        page = current_post.page
        if page.owner.pk == request.user.id:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            publish("update_post", current_post.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Impossible to alter a foreign page'},
                            status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        delete_post = self.get_object()
        page = delete_post.page
        if page.owner.pk == request.user.id:
            publish("delete_post", delete_post.pk)
            self.perform_destroy(delete_post)
            return Response({'message': 'Post has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Impossible to delete a foreign post'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        current_tweet = self.get_object()
        if 'action' in request.data:
            action_serializer = LikeActionSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get('action')
            if action == 'LIKE':
                current_tweet.likes.add(request.user)
            if action == 'UNLIKE':
                current_tweet.likes.remove(request.user)

        post_serializer = PostSerializer(data=request.data, instance=current_tweet, partial=True,
                                         context={'request', request})
        if not post_serializer.is_valid():
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post_serializer.save()
        publish("update_post", post_serializer.data['pk'])
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def create_table(self, request, *args, **kwargs):
        publish("create_table_posts")
        return Response({'message': "Posts dynamodb table created"},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def transmit(self, request, *args, **kwargs):
        try:
            publish("transmit_posts")
            return Response({'message': "Existing posts transmitted to dynamodb"},
                            status=status.HTTP_200_OK)
        except:
            return Response({'message': "Table Posts doesn't exist"},
                            status=status.HTTP_200_OK)
