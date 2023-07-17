from django.db import models
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, OwnerSerializer, EmployeeSerializer, CustomerSerializer
)
from app1.models import Owner, Employee, Customer
from auth_app.business_rules import registration


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        return registration.register_user(user, self.serializer_class)

        # user = request.data.get('user', {})

        # # Паттерн создания сериализатора, валидации и сохранения - довольно
        # # стандартный, и его можно часто увидеть в реальных проектах.
        # serializer = self.serializer_class(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        # if user['user_level'] == 'owner':
        #     Owner.objects.create(name=user['username'])
        # elif user['user_level'] == 'employee':
        #     Employee.objects.create(name=user['username'], owner=None)
        # elif user['user_level'] == 'customer':
        #     Customer.objects.create(name=user['username'])

        # return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        owner = Owner.objects.filter(name=request.user.username)
        employee = Employee.objects.filter(name=request.user.username)
        customer = Customer.objects.filter(name=request.user.username)

        if len(owner):
            response = {
                "serializer": serializer.data,
                "owner": OwnerSerializer(owner[0]).data
            }
        elif len(employee):
            response = {
                "serializer": serializer.data,
                "employee": EmployeeSerializer(employee[0]).data
            }
        elif len(customer):
            response = {
                "serializer": serializer.data,
                "customer": CustomerSerializer(customer[0]).data
            }

        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
