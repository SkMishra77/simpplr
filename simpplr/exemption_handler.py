import rest_framework.exceptions
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from simpplr.utils import response_fun


def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response.
    response = exception_handler(exc, context)
    errors = []
    if isinstance(exc, rest_framework.exceptions.ValidationError) and hasattr(exc, 'detail'):
        for i, error in exc.__dict__['detail'].items():
            errors.append(f'{i} : {error[0]}')

        error_string = "  ".join(errors)
        response = response_fun(0, error_string)
        return response

    if isinstance(exc, APIException):
        response = response_fun(0, exc.detail, status_code=exc.status_code)
        return response

    if hasattr(exc, 'args') and exc.args:
        response = response_fun(0, exc.args[0])

    return response
