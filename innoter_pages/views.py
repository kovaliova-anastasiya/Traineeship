from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from innoter_pages.models import Page
from innoter_pages.serializers import ShowFollowersSerializer, \
    ShowRequestsSerializer, ShowTagsAttachedSerializer, PageRetrieveSerializer, ShowPostsOnPageSerializer
from innoter_pages.serializers import PageListSerializer, \
    PageCreateSerializer, PageUpdateSerializer, \
    PageSerializer
from innoter_pages.follow_action import FollowActionSerializer
from innoter_user.models import User
from innoter_pages.approve_action import ApproveActionSerializer
from innoter_pages.block_action import BlockActionSerializer
from rest_framework.decorators import action

from innoter_user.permissions import UserIsOwner, RoleIsAdmin, RoleIsModerator


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

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all(self, request, *args, **kwargs):
        serializer = PageListSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def info(self, request, *args, **kwargs):
        current_page = self.get_object()
        serializer = PageRetrieveSerializer(current_page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_new(self, request, *args, **kwargs):
        print(request.data)
        serializer = PageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[UserIsOwner])
    def upd(self, request, *args, **kwargs):
        update_my_page = self.get_object()
        serializer = PageUpdateSerializer(instance=update_my_page, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], permission_classes=[UserIsOwner | RoleIsAdmin | RoleIsModerator])
    def delete(self, request, *args, **kwargs):
        delete_page = self.get_object()
        self.perform_destroy(delete_page)
        return Response({'message': 'Page has been deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def show_attached_tags(self, request, *args, **kwargs):
        current_page = self.get_object()
        show_tags_serializer = ShowTagsAttachedSerializer(current_page)
        return Response(show_tags_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def show_posts(self, request, *args, **kwargs):
        current_page = self.get_object()
        posts_on_page_serializer = ShowPostsOnPageSerializer(current_page)
        return Response(posts_on_page_serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def show_followers(self, request, *args, **kwargs):
        current_page = self.get_object()
        followers_serializer = ShowFollowersSerializer(current_page)
        return Response(followers_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def show_requests(self, request, *args, **kwargs):
        current_page = self.get_object()
        requests_serializer = ShowRequestsSerializer(current_page)
        return Response(requests_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def follow(self, request, *args, **kwargs):
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

    @action(detail=True, methods=['patch'], permission_classes=[UserIsOwner])
    def manage_requests(self, request, *args, **kwargs):
        current_page = self.get_object()

        if 'action' in request.data:
            action_serializer = ApproveActionSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get('action')

            potential_follower_pk = action_serializer.data.get('request_pk')
            print(current_page.follow_requests.get(id=potential_follower_pk))
            try:
                if action == 'APPROVE':
                    current_page.followers.add(current_page.follow_requests.get(id=potential_follower_pk))
                    current_page.follow_requests.remove(current_page.follow_requests.get(id=potential_follower_pk))
                if action == 'REJECT':
                    current_page.follow_requests.remove(current_page.follow_requests.get(potential_follower_pk))
            except User.objects.get(id=potential_follower_pk).DoesNotExist:
                return Response({'message': "This user wasn't going to follow this page"},
                                status=status.HTTP_404_NOT_FOUND)

        page_serializer = PageSerializer(data=request.data, instance=current_page, partial=True,
                                         context={'request', request})
        if not page_serializer.is_valid():
            return Response(page_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        page_serializer.save()
        return Response(page_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[RoleIsAdmin | RoleIsModerator])
    def block_page(self, request, *args, **kwargs):
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
