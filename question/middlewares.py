from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

import os


class MainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path != "/help/" and request.headers.get("identity", "").upper() != os.environ.get("IDENTITY", False):
            return JsonResponse(status=403, data={"error": "permission denied"})
