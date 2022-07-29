from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from question.permissions import TeachersOnly, StudentsOnly
from .models import Question, User
from .serializers import UserSerializer, QuestionSerializer


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.password = make_password(request.data.get("password"))
        user.save()
        return Response(status=201)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def login(self, request):
        data = request.data
        try:
            user = User.objects.get(username=data.get("username"))
            if not check_password(data.get("password"), user.password):
                raise ValueError
        except (User.DoesNotExist, ValueError):
            return Response({"error": "Invalid username or password"}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
        user = User.objects.get(id=pk)
        return Response({"user": UserSerializer(user).data})


class TeacherViewSet(viewsets.ViewSet):
    permission_classes = [TeachersOnly]

    def list(self, request):
        questions = Question.objects.filter(teacher=request.user)
        return Response(QuestionSerializer(questions, many=True).data)

    def create(self, request):
        data = request.data.copy()
        data["teacher"] = request.user.id
        serializer = QuestionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def partial_update(self, request, pk):
        data = request.data.copy()
        question = Question.objects.get(teacher=request.user, id=pk)
        serializer = QuestionSerializer(data=data, instance=question, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def retrieve(self, request, pk):
        question = Question.objects.get(teacher=request.user, id=pk)
        return Response(QuestionSerializer(question).data)

    def destroy(self, request, pk):
        Question.objects.get(teacher=request.user, id=pk).delete()
        return Response(status=204)


class StudentViewSet(viewsets.ViewSet):
    permission_classes = [StudentsOnly]

    def list(self, request):
        teacher_id = request.GET.get("teacher")
        teacher = User.objects.get(id=teacher_id, student=False)
        questions = Question.objects.filter(teacher=teacher).exclude(answer__student=request.user, answer__completed=True)
        return Response(QuestionSerializer(questions, many=True).data)

    def create(self, request):
        pass
