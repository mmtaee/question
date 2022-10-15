from rest_framework.decorators import api_view
from rest_framework.response import Response

auth = {
    "register": {
        "request": {
            "method": "POST",
            "path": "register/",
            "authentication": False,
            "data": ["first_name", "last_name", "username", "password", "student{BOOLEAN}"],
        },
        "response": {"status_codes": [201, 400], "data": None},
    },
    "login": {
        "request": {
            "method": "POST",
            "path": "login/",
            "authentication": False,
            "data": ["username", "password"],
        },
        "response": {"status_codes": [200, 400], "data": ["token", "user"]},
    },
    "profile": {
        "request": {
            "method": "GET",
            "path": "{USERID}/profile/",
        },
        "response": {"status_codes": [200, 404], "data": ["user"]},
    },
}

teacher = {
    "questions": {
        "request": {
            "method": "GET",
            "path": "/",
        },
        "response": {"status_codes": [20, 404], "data": "questions"},
    },
    "create_question": {
        "request": {
            "method": "POST",
            "path": "/",
            "data": ["format", "question", "choice{optional}", "teacher_answer", "point{1-5}"],
        },
        "response": {"status_codes": [201, 400], "data": "question"},
    },
    "destroy_question": {
        "request": {
            "method": "DELETE",
            "path": "{QUESTIONPK}/",
        },
        "response": {"status_codes": [204, 404], "data": None},
    },
    "students_list": {
        "request": {
            "method": "GET",
            "path": "/students/",
        },
        "response": {"status_codes": [200, 404], "data": "students"},
    },
    "answers_list": {
        "request": {
            "method": "GET",
            "path": "{STUDENTPK}/answers/",
        },
        "response": {"status_codes": [200, 404], "data": "answers"},
    },
    "pointing": {
        "request": {
            "method": "POST",
            "path": "{STUDENTPK}/answers/",
            "data": ["student", "answers{ answer_pk : point }"],
        },
        "response": {"status_codes": [200, 404], "data": "answers"},
    },
}

student = {
    "questions_list": {
        "request": {
            "method": "GET",
            "path": "{TEACHERID}/questions/",
        },
        "response": {"status_codes": [200, 404], "data": ["questions"]},
    },
    "answer": {
        "request": {
            "method": "POST",
            "path": "answer/",
            "data": ["teacher", "questions : { question_pk : answer }"],
        },
        "response": {"status_codes": [201, 404], "data": None},
    },
    "result": {
        "request": {
            "method": "GET",
            "path": "{TEACHERID}/result/",
        },
        "response": {"status_codes": [200, 404], "data": "answers"},
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
        "student": student,
    }
    return Response(data.get(_filter) if _filter else data)
