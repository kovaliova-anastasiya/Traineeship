from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from innoter_pages.models import Page
from innoter_posts.models import Post
from innoter_posts.serializers import PostListSerializer, \
    PostCreateSerializer, PostUpdateSerializer, \
    PostRetrieveSerializer, PostSerializer
from innoter_posts.like_action import LikeActionSerializer
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all(self, request, *args, **kwargs):
        serializer = PostSerializer(self.queryset, many=True)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Impossible to attach a tag to foreign page'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def upd(self, request, *args, **kwargs):
        serializer = PostUpdateSerializer(data=request.data)
        current_post = self.get_object()
        page = current_post.page
        if page.owner.pk == request.user.id:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Impossible to attach a tag to foreign page'},
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
        return Response(post_serializer.data, status=status.HTTP_200_OK)
