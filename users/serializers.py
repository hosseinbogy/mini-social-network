from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "is_private",
            "role",
            "date_joined",
        ]
        read_only_fields = ["id", "role", "date_joined"]
        
from rest_framework import serializers
from .models import Follow, UserProfile

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "status", "created_at"]
        read_only_fields = ["id", "follower", "status", "created_at"]

    def validate(self, attrs):
        req = self.context["request"]
        following = attrs["following"]
        if req.user.id == following.id:
            raise serializers.ValidationError("Cannot follow yourself.")
        return attrs