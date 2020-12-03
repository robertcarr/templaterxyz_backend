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


class MissingParameters(APIException):
    """
    Raised when specifically missing only parameters
    """
    status_code = 400
    default_detail = 'The parameters are missing.  We cannot render this template'
    default_code = 'parameters_missing'


class AccountRequired(APIException):
    """ Raised when trying to access a feature that requires account """
    status_code = 401
    default_detail = 'You must create an account to access this'
    default_code = 'account_required'


class MissingTemplateParameters(APIException):
    """ Raised when trying to render a template that is missing parameters"""
    status_code = 400
    default_detail = "Your template is missing one or more parameters"
    default_code = 'parameters_missing'


class TemplateInvalidOrMissing(APIException):
    """
    Raised when a template record exists, but the template itself is missing or invalid for some reason
    """
    status_code = 400
    default_detail = 'The template code is missing or corrupted'
    default_code = 'template_missing_or_corrupted'