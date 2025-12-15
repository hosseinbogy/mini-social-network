from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import permissions, response
from django.db.models import Q

from posts.models import Post
from users.models import Follow
from posts.serializers import PostSerializer


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        following_ids = Follow.objects.filter(
            follower=user, status=Follow.ACCEPTED
        ).values_list("following_id", flat=True)

        qs = Post.objects.select_related("author").filter(
            status="active"
        ).filter(
            Q(author=user) |
            Q(author_id__in=following_ids, visibility="public") |
            Q(author_id__in=following_ids, visibility="followers")
        ).order_by("-created_at")

        return response.Response(PostSerializer(qs, many=True).data)


class ExploreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Post.objects.select_related("author").filter(
            status="active",
            visibility="public",
        ).order_by("-created_at")

        return response.Response(PostSerializer(qs, many=True).data)