from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions as rest_permissions
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api import permissions
from api.models import Comment, Follow, Group, Post, User
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.viewsets import ListCreateViewSet


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsOwnerOrReadOnly,
        rest_permissions.IsAuthenticatedOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsOwnerOrReadOnly,
        rest_permissions.IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ListCreateViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
    )


class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)

    def perform_create(self, serializer):
        following_name = self.request.data.get('following', default=None)
        following = get_object_or_404(User, username=following_name)
        serializer.save(following=following, user=self.request.user)
