from django.shortcuts import render
from rest_framework import generics, viewsets
from innoter_components.models import Tag, Page, Post
from innoter_components.serializers import TagSerializer, PageSerializer, PostSerializer
# Create your views here.


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
