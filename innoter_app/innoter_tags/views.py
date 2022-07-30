from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from innoter_pages.models import Page
from innoter_tags.models import Tag
from innoter_tags.serializers import TagListSerializer, \
    TagCreateSerializer, TagUpdateSerializer, TagRetrieveSerializer, TagDeleteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class PageTagViewSet(viewsets.ModelViewSet):
    serializer_class = TagListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('page_pk')
        queryset = Page.objects.get(pk=pk).tags
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all(self, request, *args, **kwargs):
        serializer = TagListSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def info(self, request, *args, **kwargs):
        current_tag = self.get_object()
        serializer = TagRetrieveSerializer(current_tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_new(self, request, *args, **kwargs):
        serializer = TagCreateSerializer(data=request.data)
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
        serializer = TagUpdateSerializer(data=request.data)
        page_pk = request.data.get('page')
        page = Page.objects.get(pk=page_pk)
        if page.owner.pk == request.user.id:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Impossible to change a tag on a foreign page'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        tag = self.get_object()
        serializer = TagDeleteSerializer(data=request.data)
        page_pk = request.data.get('page')
        page = Page.objects.get(pk=page_pk)
        if page.owner.pk == request.user.id:
            serializer.is_valid(raise_exception=True)
            self.perform_destroy(tag)
            return Response({'message': 'Tag has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Impossible to delete a tag on a foreign page'},
                            status=status.HTTP_400_BAD_REQUEST)
