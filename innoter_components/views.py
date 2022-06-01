from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from innoter_components.models import Tag, Page, Post
from innoter_components.serializers import TagListSerializer, TagCreateSerializer, \
    TagUpdateSerializer, TagRetrieveSerializer
from innoter_components.serializers import PageListSerializer, PageCreateSerializer, \
    PageUpdateSerializer
from innoter_components.serializers import PostListSerializer, PostCreateSerializer, \
    PostUpdateSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_classes = {'list': TagListSerializer,
                          'create': TagCreateSerializer,
                          'update': TagUpdateSerializer,
                          'retrieve': TagRetrieveSerializer
                          }

    def get_serializer_class(self):
        print(self.action)
        serializer = self.serializer_classes.get(self.action, None)
        return serializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()

    serializer_classes = {'list': PageListSerializer,
                          'create': PageCreateSerializer,
                          'update': PageUpdateSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    serializer_classes = {'list': PostListSerializer,
                          'create': PostCreateSerializer,
                          'update': PostUpdateSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer
