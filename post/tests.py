from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from django.contrib.auth import get_user_model

POST_URL = reverse("post:post-list")


def detail_url(post_id):
    return reverse("post:post-detail", args=[post_id])


def create_post(user, content="Test content", hashtags=""):
    return Post.objects.create(user=user, content=content, hashtags=hashtags)


class UnauthenticatedPostApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedPostApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "pass1423")
        self.client.force_authenticate(self.user)

    def test_list_posts(self):
        create_post(self.user)
        post_with_hashtags = create_post(self.user, hashtags="#test")
        res = self.client.get(POST_URL)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_post(self):
        payload = {"content": "Test content", "hashtags": "#test"}
        res = self.client.post(POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data["id"])
        self.assertEqual(post.content, payload["content"])
        self.assertEqual(post.hashtags, payload["hashtags"])

    def test_retrieve_post_detail(self):
        post = create_post(self.user, hashtags="#test")
        url = detail_url(post.id)
        res = self.client.get(url)

        serializer = PostDetailSerializer(post)
        self.assertEqual(res.data, serializer.data)

    def test_update_own_post(self):
        post = create_post(self.user)
        payload = {"content": "New content"}
        url = detail_url(post.id)
        res = self.client.patch(url, payload)

        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(post.content, payload["content"])

    def test_update_other_user_post(self):
        other_user = get_user_model().objects.create_user("other@test.com", "pass1423")
        post = create_post(other_user)
        payload = {"content": "New content"}
        url = detail_url(post.id)
        res = self.client.patch(url, payload)

        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(post.content, payload["content"])

    def test_delete_own_post(self):
        post = create_post(self.user)
        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())

    def test_delete_other_user_post(self):
        other_user = get_user_model().objects.create_user("other@test.com", "pass1423")
        post = create_post(other_user)
        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=post.id).exists())
