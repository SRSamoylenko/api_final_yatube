from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions as rest_permissions
from rest_framework import status, viewsets
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response

from api import permissions
from api.models import Comment, Follow, Group, Post, User
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)


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


class GroupListCreate(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
    )


class FollowListCreate(ListCreateAPIView):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)

    def create(self, request, *args, **kwargs):
        following_name = self.request.data.get('following', None)
        exists = Follow.objects.filter(
            user=self.request.user,
            following__username=following_name
        ).exists()
        if (following_name is None
                or exists
                or following_name == self.request.user.username):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        following_name = self.request.data.get('following', None)
        following = get_object_or_404(User, username=following_name)
        serializer.save(user=self.request.user, following=following)
