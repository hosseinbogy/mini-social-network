from rest_framework import permissions, response, status, views
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

class JWTLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if not user:
            return response.Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return response.Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=200)


class JWTRefreshView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            return response.Response({"detail": "refresh is required"}, status=400)
        try:
            refresh = RefreshToken(token)
            return response.Response({"access": str(refresh.access_token)}, status=200)
        except Exception:
            return response.Response({"detail": "Invalid refresh"}, status=401)


class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        u = request.user
        return response.Response({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "bio": u.bio,
            "avatar": u.avatar,
            "is_private": u.is_private,
            "role": u.role,
        }, status=200)
        
from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Follow

class CanViewProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.is_private:
            return True
        if obj.id == request.user.id:
            return True
        return Follow.objects.filter(
            follower=request.user, following=obj, status=Follow.ACCEPTED
        ).exists()
        
class TokenLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return response.Response({"detail": "Invalid credentials"}, status=401)
        token, _ = Token.objects.get_or_create(user=user)
        return response.Response({"token": token.key}, status=200)


class TokenLogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return response.Response(status=204)