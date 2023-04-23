from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from pagination import PostsListPagination
from post.models import Post
from post.permissions import IsAuthorOrReadOnly
from post.serializers import PostSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PostsListPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        hashtags = self.request.query_params.get("tag")

        queryset = self.queryset

        if hashtags:
            queryset = queryset.filter(hashtags__icontains=hashtags)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "tag",
                type={"type": "str"},
                description="Filter by substring in hashtags(ex. ?tag=adm)"
            ),

        ]

    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
