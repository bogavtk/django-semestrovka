from django.test import TestCase
from rest_framework.exceptions import ValidationError

from auth_app.business_rules import registration
from auth_app.serializers import RegistrationSerializer


# Create your tests here.
class RegistrationTest(TestCase):
    def test_invalid_payload(self) -> None:
        self.assertRaises(ValidationError, registration.register_user, {}, RegistrationSerializer)
