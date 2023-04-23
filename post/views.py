from rest_framework import viewsets

from post.models import Post
from post.permissions import IsAdminOrIfAuthenticatedReadOnly, IsAuthorOrReadOnly
from post.serializers import PostSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return super().get_serializer_class()

