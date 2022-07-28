from rest_framework import routers
from app.api import UserViewSet

router = routers.DefaultRouter()


router.register("auth", UserViewSet, basename="auth")
