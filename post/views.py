from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from post.models import Post
from post.permissions import IsAdminOrIfAuthenticatedReadOnly
from post.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
