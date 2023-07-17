from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from auth_app.models import User
from app1.models import Promotion
from app1.models import Restaurant
from app1.serializers import PromotionSerializer


def _get_promotion(
        user: User, 
        serializer_class: SerializerMetaclass, 
        restaurant_id: int) -> Response:

    serializer = serializer_class(user)
    serialized_user = serializer.data

    if serialized_user['user_level'] != "owner":
        return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)
    
    restaurant = Restaurant.objects.filter(id=restaurant_id)

    if len(restaurant) == 0:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    if restaurant[0].owner != user:
        return Response({"error": "You are not owner of this restaurant"}, status=status.HTTP_400_BAD_REQUEST)
    
    promotions = Promotion.objects.filter(restaurant=restaurant[0])
    promotions = PromotionSerializer(promotions, many=True).data

    return Response({"promotions": promotions}, status=status.HTTP_200_OK)


def _post_promotion(
        user: User, 
        serializer_class: SerializerMetaclass,
        restaurant_id: int,
        name: str,
        image=None
    ) -> Response:
    serializer = serializer_class(user)
    serialized_user = serializer.data

    if serialized_user['user_level'] != "owner":
        return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)
    
    restaurant = Restaurant.objects.filter(id=restaurant_id)

    if len(restaurant) == 0:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    if restaurant[0].owner != user:
        return Response({"error": "You are not owner of this restaurant"}, status=status.HTTP_400_BAD_REQUEST)
    
    Promotion.objects.create(
        name=name,
        restaurant=restaurant[0],
        image=image
    )

    return Response({"success": "Promotion created"}, status=status.HTTP_201_CREATED)
