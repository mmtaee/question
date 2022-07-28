from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .models import User as UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "first_name", "last_name", "bio", "student"]
        read_only_fields = ("id",)
        write_only_fields = ("password",)


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
            user = UserModel.objects.get(username=data.get("username"))
            if not check_password(data.get("password"), user.password):
                raise ValueError
        except (UserModel.DoesNotExist, ValueError):
            return Response({"error": "Invalid username or password"}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
        user = UserModel.objects.get(id=pk)
        return Response({"user": UserSerializer(user).data})
