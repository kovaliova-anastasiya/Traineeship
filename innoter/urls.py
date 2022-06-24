"""innoter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import innoter_user.urls
from innoter_tags.urls import tag_router
from innoter_pages.urls import page_router
from innoter_posts.urls import post_router
from innoter_user.urls import user_action_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(innoter_user.urls)),
    path('', include(tag_router.urls)),
    path('', include(page_router.urls)),
    path('', include(post_router.urls)),
    path('users/', include(user_action_router.urls))
]
