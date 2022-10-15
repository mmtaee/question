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
            "path": "{USERID}/profile/",
            "authentication": True,
        },
        "response": {"status_codes": [200, 404], "data": ["user"]},
    },
}

teacher = {
    "questions": {
        "request": {
            "method": "GET",
            "path": "/",
            "authentication": True,
            "fields": None,
        },
        "response": {"status_codes": [200, 400], "data": ["list"]},
    },
    "create question": {
        "request": {
            "method": "POST",
            "path": "/",
            "authentication": True,
            "fields": ["format", "question", "choice", "teacher_answer"],
        },
        "response": {"status_codes": [200, 400], "data": ["question detail"]},
        "field help": {"format": "NUMBER=1, SMALL_TEXT=2, LONG_TEXT=3,SELECT_BOX=4,RADIO_BUTTON=5"},
    },
    "delete question": {
        "request": {
            "method": "DELETE",
            "path": "{QUESTIONID}/",
            "authentication": True,
            "fields": None,
        },
        "response": {"status_codes": [204, 404]},
    },
    "students": {
        "request": {
            "method": "GET",
            "path": "students/",
            "authentication": True,
            "fields": None,
        },
        "response": {"status_codes": [204, 404], "data": ["list"]},
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
        "teacher": teacher,
    }
    return Response(data.get(_filter) if _filter else data)
