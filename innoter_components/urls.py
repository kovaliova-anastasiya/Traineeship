from rest_framework import routers
from innoter_components.views import TagViewSet, PageViewSet, PostViewSet

tag_router = routers.SimpleRouter()
tag_router.register(r'tags', TagViewSet)  # префикс для набора маршрутов

page_router = routers.SimpleRouter()
page_router.register(r'pages', PageViewSet)

post_router = routers.SimpleRouter()
post_router.register(r'posts', PostViewSet)
