from rest_framework import viewsets, status
from rest_framework.response import Response

from innoter_pages.models import Page
from innoter_tags.models import Tag
from innoter_tags.serializers import TagListSerializer, \
    TagCreateSerializer, TagUpdateSerializer, TagRetrieveSerializer
from rest_framework.permissions import IsAuthenticated
from innoter_user import permissions


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.RoleIsUser]
    serializer_classes = {'list': TagListSerializer,
                          'create': TagCreateSerializer,
                          'update': TagUpdateSerializer,
                          'retrieve': TagRetrieveSerializer
                          }

    def get_serializer_class(self):
        print(self.action)
        serializer = self.serializer_classes.get(self.action, None)
        return serializer


class PageTagViewSet(viewsets.ModelViewSet):
    serializer_class = TagListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('page_pk')
        queryset = Page.objects.get(pk=pk).tags
        return queryset


