from rest_framework import routers
from app.api import UserViewSet, TeacherViewSet, StudentViewSet

router = routers.DefaultRouter()


router.register("auth", UserViewSet, basename="auth")
router.register("teacher", TeacherViewSet, basename="teacher")
router.register("student", StudentViewSet, basename="student")
