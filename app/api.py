from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from question.permissions import TeachersOnly, StudentsOnly
from .models import Question, User, Answer
from .serializers import UserSerializer, QuestionSerializer, AnswerSerializer


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

    # def partial_update(self, request, pk):
    #     data = request.data.copy()
    #     question = Question.objects.get(teacher=request.user, id=pk)
    #     serializer = QuestionSerializer(data=data, instance=question, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=202)

    # def retrieve(self, request, pk):
    #     question = Question.objects.get(teacher=request.user, id=pk)
    #     return Response(QuestionSerializer(question).data)

    def destroy(self, request, pk):
        Question.objects.get(teacher=request.user, id=pk).delete()
        return Response(status=204)

    @action(detail=False, methods=["GET"])
    def students(self, request):
        students = User.objects.filter(student=True)
        return Response(UserSerializer(students, many=True).data)

    @action(detail=True, methods=["GET"])
    def answers(self, request, pk=None):
        student = User.objects.get(id=pk, student=True)
        answers = student.answer_set.filter(question__teacher=request.user)
        # answers = Answer.objects.filter(student=student, question__teacher=request.user)
        return Response(AnswerSerializer(answers, many=True).data)

    @action(detail=True, methods=["POST"])
    def pointing(self, request, pk=None):
        """
        data = {
            student : "pk",
            answers : {
                answer_pk : point
            }
        }
        """
        data = request.data
        student = User.objects.get(id=data.get("student"), student=True)
        for answer, point in data.get("answers"):
            answer = Answer.objects.get(id=answer, student=student)
            answer.point = point
            answer.save()
        return Response(status=202)


class StudentViewSet(viewsets.ViewSet):
    permission_classes = [StudentsOnly]

    @action(detail=True, methods=["GET"])
    def questions(self, request, pk=None):
        questions = Question.objects.filter(teacher__id=pk).exclude(answer__completed=True)
        if questions.count():
            return Response(QuestionSerializer(questions, many=True).data)
        return Response({"error": "The student has already answered the questions"}, status=400)

    @action(detail=True, methods=["GET"])
    def result(self, request, pk=None):
        teacher = User.objects.get(id=pk, student=False)
        answers = teacher.question_set.filter(answer__student=request.user, answer__completed=True)
        return Response(AnswerSerializer(answers, many=True).data)

    @action(detail=False, methods=["POST"])
    def answer(self, request):
        """
        data = {
            teacher : "pk",
            questions : {
                question_pk : answer
            },

        }
        """
        data = request.data
        teacher = User.objects.get(id=data.get("teacher"), student=False)
        for question, answer in data.get("questions").items():
            question = Question.objects.get(id=question, teacher=teacher)
            if not question.filter(answer__student=request.user, answer__completed=True).exists():
                Answer.objects.create(
                    question=question,
                    student=request.user,
                    answer=answer,
                    completed=True,
                )
        return Response(status=201)
