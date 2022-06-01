from django.urls import path
from rest_framework import routers
from innoter_user.views import UserViewSet, MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

user_router = routers.SimpleRouter()
# user_router.register(r'', UserViewSet)
# user_router.register(r'login/', MyObtainTokenPairView, 'token_obtain_pair')
# user_router.register(r'login/refresh/', TokenRefreshView.as_view(), 'token_refresh')
# urlpatterns = user_router.urls

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='auth_register'),
]

