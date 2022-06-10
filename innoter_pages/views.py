from rest_framework import viewsets
from innoter_pages.serializers import Page
from innoter_pages.serializers import PageListSerializer, \
    PageCreateSerializer, PageUpdateSerializer, PageRetrieveSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()

    serializer_classes = {'list': PageListSerializer,
                          'create': PageCreateSerializer,
                          'update': PageUpdateSerializer,
                          'retrieve': PageRetrieveSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer
