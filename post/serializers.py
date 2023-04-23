from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "content", "created_at")
