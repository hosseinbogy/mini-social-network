from rest_framework import generics, permissions, response, status
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer
from users.permissions import IsAuthorOrReadOnly
from posts.models import Post


class PostCommentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/posts/{post_id}/comments/  -> لیست کامنت‌های اصلی (parent=None)
    POST /api/posts/{post_id}/comments/  -> ساخت کامنت روی پست
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id, parent__isnull=True).select_related("author")

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE /api/comments/{id}/
    """
    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class CommentRepliesListCreateView(APIView):
    """
    GET  /api/comments/{id}/replies/ -> لیست ریپلای‌های یک کامنت
    POST /api/comments/{id}/replies/ -> ساخت ریپلای (parent ثابت = همان کامنت)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        parent = Comment.objects.get(id=id)
        qs = Comment.objects.filter(parent=parent).select_related("author")
        ser = CommentSerializer(qs, many=True)
        return response.Response(ser.data, status=200)

    def post(self, request, id):
        parent = Comment.objects.get(id=id)
        data = request.data.copy()
        data["post"] = parent.post_id
        data["parent"] = parent.id

        ser = CommentSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save(author=request.user, post=parent.post, parent=parent)
        return response.Response(ser.data, status=status.HTTP_201_CREATED)