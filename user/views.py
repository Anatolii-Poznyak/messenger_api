from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from user.models import User
from user.serializers import UserSerializer, AuthTokenSerializer, UserDetailSerializer, UserListSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserListSerializer
    queryset = get_user_model().objects.all()
