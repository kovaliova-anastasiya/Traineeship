from rest_framework import routers
from innoter_posts.views import PostViewSet, NewViewSet


post_router = routers.SimpleRouter()
post_router.register(r'posts', NewViewSet)
