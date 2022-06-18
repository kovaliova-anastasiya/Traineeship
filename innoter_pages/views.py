from rest_framework import viewsets, status
from rest_framework.response import Response
from innoter_pages.models import Page
from innoter_pages.serializers import ShowFollowersSerializer, \
    ShowRequestsSerializer, ShowTagsAttachedSerializer
from innoter_pages.serializers import PageListSerializer, \
    PageCreateSerializer, PageUpdateSerializer, \
    PageRetrieveSerializer, PageSerializer
from innoter_tags.serializers import TagListSerializer
from innoter_pages.follow_action import FollowActionSerializer
from innoter_user.models import User
from innoter_user.serializers import ListUserSerializer, \
    UpdateUserSerializer
from innoter_pages.approve_action import ApproveActionSerializer
from innoter_pages.block_action import BlockActionSerializer
from rest_framework.decorators import action


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


# FUNCTIONALITY WITH ACTIONS
class ACTIONPageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    serializer_class_create = PageCreateSerializer

    @action(detail=True, methods=['get'])
    def show_tags(self, request, *args, **kwargs):
        current_page = self.get_object()
        show_tags_serializer = ShowTagsAttachedSerializer(current_page)
        return Response(show_tags_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def show_followers(self, request, *args, **kwargs):
        current_page = self.get_object()
        followers_serializer = ShowFollowersSerializer(current_page)
        return Response(followers_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def show_requests(self, request, *args, **kwargs):
        current_page = self.get_object()
        requests_serializer = ShowRequestsSerializer(current_page)
        return Response(requests_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def follow_page(self, request, *args, **kwargs):
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

    @action(detail=True, methods=['patch'])
    def manage_request(self, request, *args, **kwargs):
        current_page = self.get_object()

        if 'action' in request.data:
            action_serializer = ApproveActionSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get('action')

            # potential_follower_pk = kwargs.get('foll_pk')
            potential_follower_pk = action_serializer.data.get('request_pk')

            try:
                if action == 'APPROVE':
                    print(current_page.follow_requests.get(id=potential_follower_pk))
                    current_page.followers.add(current_page.follow_requests.get(id=potential_follower_pk))
                    current_page.follow_requests.remove(current_page.follow_requests.get(id=potential_follower_pk))
                if action == 'REJECT':
                    current_page.follow_requests.remove(current_page.follow_requests.get(potential_follower_pk))
            except User.objects.get(id=potential_follower_pk).DoesNotExist:
                return Response({'message': "This user wasn't going to foolow this page"},
                                status=status.HTTP_404_NOT_FOUND)

        page_serializer = PageSerializer(data=request.data, instance=current_page, partial=True,
                                         context={'request', request})
        if not page_serializer.is_valid():
            return Response(page_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        page_serializer.save()
        return Response(page_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def block_p(self, request, *args, **kwargs):
        block_page = self.get_object()

        if 'action' in request.data:
            action_serializer = BlockActionSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get('action')

            print(block_page.unblock_date)

            if action == 'BLOCK':
                block_page.unblock_date = action_serializer.data.get('unblock_date')
            if action == 'UNBLOCK':
                block_page.unblock_date = None
            print(action_serializer.data.get('unblock_date'))
            print(block_page.unblock_date)

        page_serializer = PageSerializer(data=request.data, instance=block_page, partial=True,
                                         context={'request', request})
        if not page_serializer.is_valid():
            return Response(page_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        page_serializer.save()
        return Response(page_serializer.data, status=status.HTTP_200_OK)
