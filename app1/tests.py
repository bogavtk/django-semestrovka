from random import randint
from uuid import uuid4

from django.test import TestCase

import auth_app
from app1.models import *
from auth_app.serializers import UserSerializer
from app1.business_rules.owner import promotion
from app1.business_rules.owner import restaurant

CUSTOMER = User(
    username=uuid4(),
    user_level="customer",
    email=f"{uuid4()}@{uuid4()}.{uuid4()}"
)

EMPLOYEE = User(
    username=uuid4(),
    user_level="employee",
    email=f"{uuid4()}@{uuid4()}.{uuid4()}"
)

OWNER = User(
    username=uuid4(),
    user_level="owner",
    email=f"{uuid4()}@{uuid4()}.{uuid4()}"
)


class RestaurantTest(TestCase):
    def test_customer_gets_restaurant(self):
        assert restaurant._get_restaurants(CUSTOMER, UserSerializer).status_code == 400
    
    def test_employee_gets_restaurant(self):
        assert restaurant._get_restaurants(EMPLOYEE, UserSerializer).status_code == 400
    
    def test_not_registered_owner_gets_restaurant(self):
        self.assertRaises(auth_app.models.User.DoesNotExist, restaurant._get_restaurants, OWNER, UserSerializer)

    def test_customer_creates_restaurant(self) -> None:
        assert restaurant._post_restaurants(CUSTOMER, UserSerializer, uuid4(), uuid4()).status_code == 400

    def test_employee_creates_restaurant(self) -> None:
        assert restaurant._post_restaurants(EMPLOYEE, UserSerializer, uuid4(), uuid4()).status_code == 400


class PromotionTest(TestCase):
    def test_customer_gets_promotions(self):
        assert promotion._get_promotion(CUSTOMER, UserSerializer, randint(1, 100)).status_code == 400

    def test_employee_gets_promotions(self):
        assert promotion._get_promotion(EMPLOYEE, UserSerializer, randint(1, 100)).status_code == 400

    def test_not_registered_owner_gets_promotions(self):
        assert promotion._get_promotion(OWNER, UserSerializer, randint(1, 100)).status_code == 400

    def test_customer_creates_promotions(self) -> None:
        assert promotion._post_promotion(CUSTOMER, UserSerializer, uuid4(), uuid4()).status_code == 400

    def test_employee_creates_promotions(self) -> None:
        assert promotion._post_promotion(EMPLOYEE, UserSerializer, uuid4(), uuid4()).status_code == 400

