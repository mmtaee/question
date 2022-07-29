from rest_framework import permissions, status
from rest_framework.exceptions import APIException

from django.utils.translation import gettext_lazy as _


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("You do not have permission to perform this action.")
    default_code = "permission_denied"


class TeachersOnly(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if not request.user.is_student:
            return True
        raise PermissionDenied


class StudentsOnly(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if request.user.is_student:
            return True
        raise PermissionDenied
