from rest_framework import routers
from innoter_pages.views import ACTIONPageViewSet

page_router = routers.SimpleRouter()
page_router.register(r'pages', ACTIONPageViewSet)

