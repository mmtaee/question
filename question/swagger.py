from rest_framework.decorators import api_view
from rest_framework.response import Response

auth = {
    "register": {
        "request": {
            "method": "POST",
            "path": "register/",
            "authentication": False,
            "fields": ["first_name", "last_name", "username", "password", "student{BOOLEAN}"],
        },
        "response": {"status_codes": [201, 400], "data": None},
    },
    "login": {
        "request": {
            "method": "POST",
            "path": "login/",
            "authentication": False,
            "fields": ["username", "password"],
        },
        "response": {"status_codes": [200, 400], "data": ["token", "user"]},
    },
    "profile": {
        "request": {
            "method": "GET",
            "path": "profile/{USERID}/",
        },
        "response": {"status_codes": [200, 404], "data": ["user"]},
    },
}


@api_view(["GET"])
def swagger(request):
    _filter = request.GET.get("filter")
    data = {
        "base_url": "/api/",
        "headers": {
            "identity": "IDENTITY",
            "Authorization": "Authorization: Token TOKEN_RECIVED_FROM_BACKEND_AT_LOGIN",
        },
        "auth": auth,
    }
    return Response(data.get(_filter) if _filter else data)
