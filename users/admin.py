from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile

class UserProfileCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ("username", "email", "first_name", "last_name", "bio", "avatar", "is_private", "role")

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1") or ""
        p2 = cleaned.get("password2") or ""
        if len(p1) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if p1 != p2:
            raise ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username", "email", "first_name", "last_name", "bio", "avatar", "is_private", "role")

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreateForm
    form = UserProfileChangeForm
    model = UserProfile

    list_display = ("id", "username", "email", "role", "is_private", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("role", "is_private", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "email")}),
        ("Profile", {"fields": ("first_name", "last_name", "bio", "avatar", "is_private", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "bio", "avatar", "is_private", "role", "password1", "password2"),
        }),
    )

    ordering = ("id",)