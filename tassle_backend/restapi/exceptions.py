from rest_framework.exceptions import APIException


class MissingTemplateOrParams(APIException):
    """
    Raised when posting a template but missing the actual template data or params to merge with
    """
    status_code = 400
    default_detail = 'The template file or params are missing'
    default_code = 'template_or_params_missing'


class TemplateNotFound(APIException):
    """
    Raised when the template is not found by UUID
    """
    status_code = 404
    default_detail = 'The template was not found'
    default_code = 'template_not_found'


class InvalidParameterFormat(APIException):
    """
    Raised when parameters are not submitted as proper JSON
    """
    status_code = 400
    default_detail = "Parameters must be in valid JSON format"
    default_code = 'invalid_parameter_format'