from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserRoles
from .permissions import IsAdminPermission
from .serializers import (RegisterUserSerializer, TokenRefreshSerializer,
                          UserSerializer)


class CreateUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_user = get_object_or_404(User, email=request.data['email'])
            confirmation_code = str(RefreshToken.for_user(new_user))
            send_mail(
                'Код подтверждения',
                f'Ваш код: {confirmation_code}',
                'from@example.com',
                [f'{new_user.email}'],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtain(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('confirmation_code')
        if not username or not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not default_token_generator.check_token(user, code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAPiViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(request.user, request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.user)
        if (serializer.validated_data.get('role')
                and serializer.validated_data['role'] != user.role):
            if request.user.role != UserRoles.ADMIN:
                serializer.validated_data['role'] = user.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
