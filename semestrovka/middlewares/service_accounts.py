from rest_framework.exceptions import ValidationError

from auth_app.business_rules import registration
from auth_app.serializers import RegistrationSerializer


def create_service_accounts(get_response) -> None:
    def middleware(request):
        response = get_response(request)

        employee = {
            "email": "_service_account_employee@ya.ru",
            "username": "_service_account_employee",
            "password": "4a1b2832-2506-4faa-9cae-57e406ebf720",
            "user_level": "employee",
        }
        customer = {
            "email": "_service_account_customer@ya.ru",
            "username": "_service_account_customer",
            "password": "2fb7ce54-bbdb-4a4e-8a52-d3dc5fa096b9",
            "user_level": "customer",
        }

        try:
            registration.register_user(employee, RegistrationSerializer)
        except ValidationError:
            pass

        try:
            registration.register_user(customer, RegistrationSerializer)
        except ValidationError:
            pass

        return response

    return middleware
