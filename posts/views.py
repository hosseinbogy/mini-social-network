from django.db.models import Q
from rest_framework import viewsets, decorators, response, status, filters
from rest_framework.permissions import IsAuthenticated
from users.models import Follow
from .models import Post, Like
from .serializers import PostSerializer
from users.permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    def get_queryset(self):
        user = self.request.user

        following_ids = Follow.objects.filter(
            follower=user, status=Follow.ACCEPTED
        ).values_list("following_id", flat=True)

        qs = Post.objects.select_related("author").filter(status="active").filter(
            Q(visibility="public") |
            Q(author=user) |
            Q(visibility="followers", author_id__in=following_ids)
        )

        author = self.request.query_params.get("author")
        visibility = self.request.query_params.get("visibility")
        if author:
            qs = qs.filter(author_id=author)
        if visibility:
            qs = qs.filter(visibility=visibility)

        return qs.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @decorators.action(detail=True, methods=["post"], url_path="like")
    def like_toggle(self, request, pk=None):
        post = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            obj.delete()
            return response.Response({"liked": False}, status=status.HTTP_200_OK)
        return response.Response({"liked": True}, status=status.HTTP_201_CREATED)