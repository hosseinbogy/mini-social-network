from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "content", "parent", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "author_username", "created_at", "updated_at", "post", "parent"]

    def validate_content(self, v):
        if not (1 <= len(v) <= 500):
            raise serializers.ValidationError("Comment content must be 1..500 chars.")
        return v

    def validate(self, attrs):
        parent = attrs.get("parent")
        post = attrs.get("post")
        if parent and parent.post_id != post.id:
            raise serializers.ValidationError("Parent comment must belong to the same post.")
        return attrs