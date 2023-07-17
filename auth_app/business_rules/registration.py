from rest_framework import status
from rest_framework.response import Response

from app1.models import *


def register_user(user, serializer_class):
    # Паттерн создания сериализатора, валидации и сохранения - довольно
    # стандартный, и его можно часто увидеть в реальных проектах.
    serializer = serializer_class(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if user['user_level'] == 'owner':
        Owner.objects.create(name=user['username'])
    elif user['user_level'] == 'employee':
        Employee.objects.create(name=user['username'], owner=None)
    elif user['user_level'] == 'customer':
        Customer.objects.create(name=user['username'])

    return Response(serializer.data, status=status.HTTP_201_CREATED)
