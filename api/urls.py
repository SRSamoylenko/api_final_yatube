from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (CommentViewSet, FollowListCreate, GroupListCreate,
                       PostViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'posts',
    PostViewSet,
    basename='Post'
)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='Comment'
)

urlpatterns = [
    re_path(
        r'^(?P<version>v1)/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    re_path(
        r'^(?P<version>v1)/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    re_path(
        r'^(?P<version>v1)/',
        include(router_v1.urls)
    ),
    re_path(
        r'^(?P<version>v1)/group/',
        GroupListCreate.as_view(),
        name='group_list_create'
    ),
    re_path(
        r'^(?P<version>v1)/follow/',
        FollowListCreate.as_view(),
        name='follow_list_create'
    ),
]
