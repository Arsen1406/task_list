from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from api import serializers
from api.permissions import AdminOnly
from core.tasks import change_status_task
from tasks.models import Task

User = get_user_model()

CREATE = 'create'
PROCESSING = 'processing'
ANSWER = 'answer'


class TasksViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.TasksSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        obj = Task.objects.create(user=self.request.user)
        request.data['number'] = obj.number
        request.data['status'] = obj.status

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ProcessingViewsSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    serializer_class = serializers.TasksSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user, status=CREATE)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == ANSWER:
            return Response(data='Данная задача уже исполнена!')
        change_status_task(instance, PROCESSING)
        return Response('Процесс обработки запущен!')


class AnswerViewsSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    serializer_class = serializers.TasksSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user, status=PROCESSING)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == CREATE:
            return Response(data='Перед ответом необходимо обработать задачу!')
        if instance.status == ANSWER:
            return Response(data='Данная задача уже исполнена!')
        change_status_task(instance, ANSWER)
        return Response('Процесс обработки запущен!')


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer
    permission_classes = [AdminOnly]
    search_fields = ('username',)
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.kwargs['username'] = self.request.user.username
        if self.request.method == 'PATCH':
            return self.update(request, partial=True, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = User
    lookup_field = 'username'
    serializer_class = serializers.TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        password = request.data.get('password')

        if password and user.password == password:
            token = str(RefreshToken.for_user(user).access_token)
            return Response(data={'token': token}, status=status.HTTP_200_OK)
        return Response(
            data='Вы не предоставили пароль!',
            status=status.HTTP_403_FORBIDDEN
        )
