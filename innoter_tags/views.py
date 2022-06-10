from rest_framework import viewsets
from innoter_tags.models import Tag
from innoter_tags.serializers import TagListSerializer, \
    TagCreateSerializer, TagUpdateSerializer, TagRetrieveSerializer
from rest_framework.permissions import IsAuthenticated


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
