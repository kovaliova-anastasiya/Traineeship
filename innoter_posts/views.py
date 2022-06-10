from rest_framework import viewsets
from innoter_posts.models import Post
from innoter_posts.serializers import PostListSerializer, \
    PostCreateSerializer, PostUpdateSerializer, PostRetrieveSerializer



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    serializer_classes = {'list': PostListSerializer,
                          'create': PostCreateSerializer,
                          'update': PostUpdateSerializer,
                          'retrieve': PostRetrieveSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer
