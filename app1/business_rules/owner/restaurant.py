from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from app1.models import User
from app1.models import Restaurant
from app1.serializers import RestaurantSerializer


def _get_restaurants(user: User, serializer_class: SerializerMetaclass) -> Response:
    serializer = serializer_class(user)

    user = serializer.data

    if user['user_level'] != "owner":
        return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)

    owner = User.objects.get(username=user["username"])
    restaurants = Restaurant.objects.filter(owner=owner)
    restaurants = RestaurantSerializer(restaurants, many=True).data

    return Response({"restaurants": restaurants}, status=status.HTTP_200_OK)


def _post_restaurants(
        user: User, 
        serializer_class: SerializerMetaclass, 
        name: str, 
        address: str) -> Response:
    serializer = serializer_class(user)

    serialized_user = serializer.data

    if serialized_user['user_level'] != "owner":
        return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)
    
    Restaurant.objects.create(
        name=name,
        address=address,
        owner=user
    )

    return Response({"success": "Restaurant created"}, status=status.HTTP_201_CREATED)
