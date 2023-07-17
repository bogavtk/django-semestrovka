from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from auth_app.models import User
from app1.models import *
from auth_app.renderers import UserJSONRenderer
from auth_app.serializers import *
from app1.serializers import *

from app1.business_rules.owner import promotion
from app1.business_rules.owner import restaurant


class RestaurantAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return restaurant._get_restaurants(request.user, self.serializer_class)

    def post(self, request, *args, **kwargs):
        name = request.data.get('name'),
        address = request.data.get('address')

        return restaurant._post_restaurants(
            request.user, 
            self.serializer_class,
            name,
            address
        )


class MenuAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # get menu instance
        serializer = self.serializer_class(request.user)
        user = serializer.data

        if user['user_level'] != "owner":
            return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)
        
        restaurant = Restaurant.objects.filter(id=request.data.get('restaurant_id'))

        if len(restaurant) == 0:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if restaurant[0].owner != request.user:
            return Response({"error": "You are not owner of this restaurant"}, status=status.HTTP_400_BAD_REQUEST)
        
        menus = Menu.objects.filter(restaurant=restaurant[0])
        menus = MenuSerializer(menus, many=True).data

        return Response({"menus": menus}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # create menu instance

        serializer = self.serializer_class(request.user)
        user = serializer.data

        if user['user_level'] != "owner":
            return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)
        
        restaurant = Restaurant.objects.filter(id=request.data.get('restaurant_id'))

        if len(restaurant) == 0:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if restaurant[0].owner != request.user:
            return Response({"error": "You are not owner of this restaurant"}, status=status.HTTP_400_BAD_REQUEST)
        
        Menu.objects.create(
            name=request.data.get('name'),
            restaurant=restaurant[0]
        )

        return Response({"success": "Menu created"}, status=status.HTTP_201_CREATED)


class PromotionsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        restaurant_id = request.GET.get('restaurant_id')
        
        response = promotion._get_promotion(
            request.user, 
            self.serializer_class, 
            restaurant_id 
        )
        print(type(response))
        return response
        
        serializer = self.serializer_class(request.user)
        user = serializer.data

        if user['user_level'] != "owner":
            return Response({"error": "You are not owner"}, status=status.HTTP_400_BAD_REQUEST)
        
        restaurant = Restaurant.objects.filter(id=request.data.get('restaurant_id'))

        if len(restaurant) == 0:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if restaurant[0].owner != request.user:
            return Response({"error": "You are not owner of this restaurant"}, status=status.HTTP_400_BAD_REQUEST)
        
        promotions = Promotion.objects.filter(restaurant=restaurant[0])
        promotions = PromotionSerializer(promotions, many=True).data

        return Response({"promotions": promotions}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return promotion._post_promotion(
            request.user,
            self.serializer_class,
            request.data.get('restaurant_id'),
            request.data.get('name'),
            request.data.get('image'),
        )


class IncreaseBalanceAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    PERCENTAGE = 0.1

    def post(self, request, *args, **kwargs):
        global PERCENTAGE
        serializer = self.serializer_class(request.user)
        user = serializer.data

        if user['user_level'] != "employee":
            return Response({"error": "You are not the employee"}, status=status.HTTP_400_BAD_REQUEST)
        
        # get customer id

        customer = Customer.objects.filter(id=request.data.get('customer_id'))

        if len(customer) == 0:
            return Response({"error": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        customer = CustomerSerializer(customer[0]).data

        # get his spending

        customer.balance += customer.spent * PERCENTAGE
        customer.save()

        return Response({"success": "Balance increased"}, status=status.HTTP_200_OK)
