from rest_framework import serializers
from .models import Post, Like, PostMedia

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ["id","author","author_username","content","visibility","status","likes_count","created_at","updated_at"]
        read_only_fields = ["id","author","author_username","likes_count","created_at","updated_at"]

    def validate_content(self, v):
        if not (1 <= len(v) <= 2000):
            raise serializers.ValidationError("Post content must be 1..2000 chars.")
        return v

    def validate_visibility(self, v):
        if v not in ("public", "followers", "private"):
            raise serializers.ValidationError("Visibility must be public|followers|private.")
        return v