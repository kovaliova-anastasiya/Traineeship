from rest_framework import routers
from innoter_tags.views import TagViewSet

tag_router = routers.SimpleRouter()
tag_router.register(r'tags', TagViewSet)  # префикс для набора маршрутов