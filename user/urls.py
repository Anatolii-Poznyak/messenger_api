from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


from user.views import CreateUserView, ManageUserView, UserListViewSet, UserDetailViewSet

app_name = "user"

router = DefaultRouter()
router.register("", UserListViewSet, basename="user-list")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("<int:pk>/", UserDetailViewSet.as_view({"get": "retrieve"}), name="user-detail"),
    path("", include(router.urls)),
]
