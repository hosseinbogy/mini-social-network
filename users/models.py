from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserProfile(AbstractUser):
    ROLE_USER = "user"
    ROLE_ADMIN = "admin"
    ROLE_MOD = "moderator"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_MOD, "Moderator"),
    ]

    email = models.EmailField(unique=True)

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(r"^[a-zA-Z0-9_]+$", "Only letters, numbers, underscore.")],
    )

    bio = models.CharField(max_length=160, blank=True)
    avatar = models.URLField(blank=True)  # later: ImageField
    is_private = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    REQUIRED_FIELDS = ["email"]

    def str(self):
        return self.username
from django.db import models

class Follow(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"
    STATUS_CHOICES = [(PENDING, "Pending"), (ACCEPTED, "Accepted")]

    follower = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="following_rel")
    following = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="followers_rel")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACCEPTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="unique_follow_pair"),
        ]