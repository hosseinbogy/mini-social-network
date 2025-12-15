from django.db import models
from users.models import UserProfile

class Post(models.Model):
    VIS_PUBLIC = "public"
    VIS_FOLLOWERS = "followers"
    VIS_PRIVATE = "private"
    VIS_CHOICES = [(VIS_PUBLIC, "Public"), (VIS_FOLLOWERS, "Followers"), (VIS_PRIVATE, "Private")]

    STATUS_ACTIVE = "active"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [(STATUS_ACTIVE, "Active"), (STATUS_ARCHIVED, "Archived")]

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    visibility = models.CharField(max_length=12, choices=VIS_CHOICES, default=VIS_PUBLIC)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_like_pair"),
        ]

class PostMedia(models.Model):
    MEDIA_IMAGE = "image"
    MEDIA_VIDEO = "video"
    MEDIA_CHOICES = [(MEDIA_IMAGE, "Image"), (MEDIA_VIDEO, "Video")]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    file_url = models.URLField()
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)