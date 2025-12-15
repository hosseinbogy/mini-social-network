from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from comments.views import PostCommentListCreateView, CommentDetailView, CommentRepliesListCreateView
from users.views import ProfileViewSet
from users.views_auth import JWTLoginView, JWTRefreshView, MeView
from users.views import FollowViewSet
from feed.views import FeedView, ExploreView
from users.views_auth import TokenLoginView, TokenLogoutView




router = DefaultRouter()
from posts.views import PostViewSet
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"profiles", ProfileViewSet, basename="profiles")
router.register(r"follows", FollowViewSet, basename="follows")

urlpatterns = [
    
    path("api/posts/<int:post_id>/comments/", PostCommentListCreateView.as_view()),
    path("api/comments/<int:pk>/", CommentDetailView.as_view()),
    path("api/comments/<int:id>/replies/", CommentRepliesListCreateView.as_view()),
    path("admin/", admin.site.urls),
    path("api/feed/", FeedView.as_view()),
    path("api/explore/", ExploreView.as_view()),
    path("api/auth/token-login/", TokenLoginView.as_view()),
    path("api/auth/token-logout/", TokenLogoutView.as_view()),
    # API
    path("api/", include(router.urls)),

    # Auth
    path("api/auth/jwt-login/", JWTLoginView.as_view()),
    path("api/auth/jwt-refresh/", JWTRefreshView.as_view()),
    path("api/auth/me/", MeView.as_view()),

]