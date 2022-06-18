from django.urls import path
from rest_framework import routers
from innoter_pages.views import PageViewSet, ACTIONPageViewSet

# page_router = routers.SimpleRouter()
# page_router.register(r'pages', NewPageViewSet)

page_router = routers.SimpleRouter()
page_router.register(r'pages', ACTIONPageViewSet)

