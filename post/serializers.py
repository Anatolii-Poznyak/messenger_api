from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "content", "created_at", "user")
