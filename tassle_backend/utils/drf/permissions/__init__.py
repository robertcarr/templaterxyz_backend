"""
Customized Permissions for django_rest_framework
"""
from rest_framework.permissions import BasePermission


class CreateTemplates(BasePermission):
    """
    Allow anyone to create perm
    """