from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from api import serializers

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser,]
    search_fields = ('username',)
    queryset = User.objects.all()

    @action(
        detail=False, methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        self.kwargs['username'] = self.request.user
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
