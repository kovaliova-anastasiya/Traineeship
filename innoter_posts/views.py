from rest_framework import viewsets, status
from innoter_posts.models import Post
from innoter_posts.serializers import PostListSerializer, \
    PostCreateSerializer, PostUpdateSerializer, \
    PostRetrieveSerializer, PostSerializer
from innoter_posts.like_action import LikeActionSerializer
from rest_framework.response import Response



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    serializer_classes = {'list': PostSerializer,
                          'create': PostCreateSerializer,
                          'update': PostUpdateSerializer,
                          'retrieve': PostSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer


class NewViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    serializer_class_create = PostCreateSerializer

    def partial_update(self, request, *args, **kwargs):
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
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class_create
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'list':
            user_id = self.request.query_params.get('user_id', None)
            if user_id:
                return Post.objects.filter(user__uuid=user_id)
        return Post.objects.all()

