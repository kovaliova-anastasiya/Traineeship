from django.urls import path
from rest_framework import routers
from innoter_pages.views import PageViewSet, MyFollowersOverview, \
    MyFollowRequestsOverview, ApproveFollowRequestView, BlockPageView
from innoter_pages.views import PageTagsViewSet, NewPageViewSet

page_router = routers.SimpleRouter()
page_router.register(r'pages', NewPageViewSet)

urlpatterns = [
    path('pages/<int:page_pk>/tags/', PageTagsViewSet.as_view({'get': 'list'})),
    path('pages/<int:page_pk>/followers/', MyFollowersOverview.as_view({'get': 'list'})),
    path('pages/<int:page_pk>/follow_requests/', MyFollowRequestsOverview.as_view({'get': 'list'})),
    path('pages/<int:pk>/follow_requests/<int:foll_pk>/',
         ApproveFollowRequestView.as_view({'patch': 'partial_update'})),
    path('pages/<int:pk>/block/', BlockPageView.as_view({'patch': 'partial_update'}))
]
