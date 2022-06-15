from rest_framework import viewsets, status
from rest_framework.response import Response
from innoter_pages.models import Page
from innoter_pages.serializers import OverviewFollowersSerializer, \
OverviewRequestsSerializer
from innoter_pages.serializers import PageListSerializer, \
    PageCreateSerializer, PageUpdateSerializer, \
    PageRetrieveSerializer, PageSerializer
from innoter_tags.serializers import TagListSerializer
from innoter_pages.follow_action import FollowActionSerializer
from innoter_user.serializers import ListUserSerializer, \
    UpdateUserSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()

    serializer_classes = {'list': PageListSerializer,
                          'create': PageCreateSerializer,
                          'update': PageUpdateSerializer,
                          'retrieve': PageSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer


class NewPageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    serializer_class_create = PageCreateSerializer

    def partial_update(self, request, *args, **kwargs):
        current_page = self.get_object()
        if 'action' in request.data:
            action_serializer = FollowActionSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get('action')
            if action == 'FOLLOW':
                if not current_page.is_private:
                    current_page.followers.add(request.user)
                else:
                    current_page.follow_requests.add(request.user)
            if action == 'UNFOLLOW':
                current_page.followers.remove(request.user)
                current_page.follow_requests.remove(request.user)

        page_serializer = PageSerializer(data=request.data, instance=current_page, partial=True,
                                           context={'request', request})
        if not page_serializer.is_valid():
            return Response(page_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        page_serializer.save()
        return Response(page_serializer.data, status=status.HTTP_200_OK)


class PageTagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('page_pk')
        queryset = Page.objects.get(pk=pk).tags
        return queryset


class MyFollowersOverview(viewsets.ModelViewSet):
    serializer_class = ListUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('page_pk')
        current_page = Page.objects.get(pk=pk)
        followers = current_page.followers
        return followers


class MyFollowRequestsOverview(viewsets.ModelViewSet):
    serializer_class = ListUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('page_pk')
        current_page = Page.objects.get(pk=pk)
        request_users = current_page.follow_requests
        return request_users


class ApproveFollowRequestView(viewsets.ModelViewSet):
    pass