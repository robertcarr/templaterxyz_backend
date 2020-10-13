from rest_framework.exceptions import APIException


class MissingTemplateOrParams(APIException):
    """
    Raised when posting a template but missing the actual template data or params to merge with
    """
    status_code = 400
    default_detail = 'The template file or params are missing.'
    default_code = 'template_or_params_missing'