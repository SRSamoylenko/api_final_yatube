from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api import views

router_v1 = DefaultRouter()
router_v1.register(
    'posts',
    views.PostViewSet,
    basename='Post',
)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='Comment',
)
router_v1.register(
    r'group',
    views.GroupViewSet,
    basename='Group',
)
router_v1.register(
    r'follow',
    views.FollowViewSet,
    basename='Follow',
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
]
