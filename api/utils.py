from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def handle_exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 401:
            response.data = {
                "success": False,
                "message": "Token invalid or missing"
            }
        elif response.status_code == 403:
            response.data = {
                "success": False,
                "message": "Oops! You do not have permission to access this resource"
            }

    return response
