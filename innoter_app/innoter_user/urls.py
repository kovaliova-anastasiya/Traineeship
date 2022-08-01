from django.urls import path
from rest_framework import routers
from innoter_user.views import UserViewSet, MyObtainTokenPairView, ACTIONUserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

user_router = routers.SimpleRouter()


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='auth_register'),
]

user_action_router = routers.SimpleRouter()
user_action_router.register(r'', ACTIONUserViewSet)

