from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from users.permissions import CanViewProfile, IsOwnerOrReadOnly
class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
from rest_framework import viewsets, decorators, response, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Follow, UserProfile
from .serializers import FollowSerializer

class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, CanViewProfile, IsOwnerOrReadOnly]

    def get_queryset(self):
        # لیست درخواست‌ها/فالوهای خود کاربر
        return Follow.objects.select_related("follower", "following").filter(follower=self.request.user)

    @decorators.action(detail=False, methods=["post"], url_path="request")
    def request_follow(self, request):
        following_id = request.data.get("following")
        if not following_id:
            return response.Response({"detail": "following is required"}, status=400)

        following = get_object_or_404(UserProfile, id=following_id)
        if following.id == request.user.id:
            return response.Response({"detail": "Cannot follow yourself"}, status=400)

        status_value = Follow.PENDING if following.is_private else Follow.ACCEPTED

        obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=following,
            defaults={"status": status_value},
        )
        if not created:
            return response.Response({"detail": "Already requested/following."}, status=400)

        return response.Response(FollowSerializer(obj).data, status=201)

    @decorators.action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        rel = get_object_or_404(Follow, id=pk)
        if rel.following_id != request.user.id:
            return response.Response({"detail": "Not allowed."}, status=403)
        rel.status = Follow.ACCEPTED
        rel.save()
        return response.Response({"status": "accepted"}, status=200)

    @decorators.action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        rel = get_object_or_404(Follow, id=pk)
        if rel.following_id != request.user.id:
            return response.Response({"detail": "Not allowed."}, status=403)
        rel.delete()
        return response.Response(status=204)

    @decorators.action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        rel = get_object_or_404(Follow, id=pk, follower=request.user)
        rel.delete()
        return response.Response(status=204)
    
from rest_framework import viewsets, decorators, response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Follow, UserProfile
from .serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.select_related("follower", "following").filter(follower=self.request.user)

    @decorators.action(detail=False, methods=["post"], url_path="request")
    def request_follow(self, request):
        following_id = request.data.get("following")
        if not following_id:
            return response.Response({"detail": "following is required"}, status=400)

        following = get_object_or_404(UserProfile, id=following_id)
        if following.id == request.user.id:
            return response.Response({"detail": "Cannot follow yourself"}, status=400)

        status_value = Follow.PENDING if following.is_private else Follow.ACCEPTED

        obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=following,
            defaults={"status": status_value},
        )
        if not created:
            return response.Response({"detail": "Already requested/following."}, status=400)

        return response.Response(FollowSerializer(obj).data, status=201)

    @decorators.action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        rel = get_object_or_404(Follow, id=pk)
        if rel.following_id != request.user.id:
            return response.Response({"detail": "Not allowed."}, status=403)
        rel.status = Follow.ACCEPTED
        rel.save()
        return response.Response({"status": "accepted"}, status=200)

    @decorators.action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        rel = get_object_or_404(Follow, id=pk)
        if rel.following_id != request.user.id:
            return response.Response({"detail": "Not allowed."}, status=403)
        rel.delete()
        return response.Response(status=204)

    @decorators.action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        rel = get_object_or_404(Follow, id=pk, follower=request.user)
        rel.delete()
        return response.Response(status=204)