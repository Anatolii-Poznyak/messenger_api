from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from post.models import Post
from post.permissions import IsAdminOrIfAuthenticatedReadOnly, IsAuthorOrReadOnly
from post.serializers import PostSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]
