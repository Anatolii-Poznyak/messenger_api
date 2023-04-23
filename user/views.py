from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, mixins, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from user.models import User
from user.serializers import UserSerializer, AuthTokenSerializer, UserDetailSerializer, UserListSerializer, \
    UserImageSerializer
from post.permissions import IsAuthorOrReadOnly


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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        name = self.request.query_params.get("name")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(first_name__icontains=name)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type={"type": "str"},
                description="Filter by substring in name(ex. ?name=adm)"
            ),

        ]

    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get("pk"))
        self.check_object_permissions(self.request, obj)
        return obj


class UserImageView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = UserImageSerializer(data=request.data)
        if serializer.is_valid():
            request.user.image = serializer.validated_data['image']
            request.user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
