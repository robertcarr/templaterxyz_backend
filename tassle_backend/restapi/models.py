import json
import uuid
import logging

from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser, AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from rest_framework.reverse import reverse, reverse_lazy

from utils.core import get_shortuuid, get_upload_folder, get_template_url
from utils.render import RenderMixin
from .exceptions import MissingTemplateOrParams

log = logging.getLogger(__name__)


class CustomUserManager(UserManager):
    def get_or_create_for_cognito(self, payload):
        cognito_id = payload['sub']
        log.debug(f'Valid JWT for sub {cognito_id}')
        user, _ = self.get_or_create(
            cognito_id=cognito_id,
            email=payload['email'],
            email_verified=payload['email_verified'],
            is_active=True
        )
        log.debug(f'cognito returning user {user}')
        return user


class Orgs(models.Model):
    """
    Basic Orgs
    """
    name = models.CharField(max_length=150, blank=False)


class Stats(models.Model):
    """
    Keep some basic stats
    """
    templates_rendered = models.BigIntegerField(default=0, blank=False)
    templates_saved = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'Stats'
        verbose_name_plural = 'Stats'


class UserProfile(models.Model):
    """
    User Profile Extension
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


class User(AbstractBaseUser, PermissionsMixin):
    created = models.DateTimeField(auto_now_add=True)
    cognito_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    username = models.CharField(max_length=30, null=True)
    api_token = models.CharField(max_length=100, default=get_shortuuid(length=30))
    email = models.EmailField(max_length=150, unique=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


class Repos(models.Model):
    """
    Repos are collection of templates that a validated user may keep templates in.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=22, default=get_shortuuid, blank=False)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    public = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Repos'
        verbose_name_plural = 'Repos'


class Templates(models.Model, RenderMixin):
    """
    Describes a Template in the system.

    The template can be public or private.
    Templates can be anonymous or owned by a registered user.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=22, default=get_shortuuid, blank=False)
    repo = models.ForeignKey(Repos, on_delete=models.CASCADE, related_name='repo', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    template = models.FileField(upload_to=get_upload_folder, blank=False)
    params = models.FileField(upload_to=get_upload_folder, blank=False)

    public = models.BooleanField(default=False)
    purge = models.BooleanField(default=False)

    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    @property
    def is_editable(self):
        """
        Can I update this template or params?
        :return: Boolean
        """
        if self.is_owner:
            return True
        else:
            return False

    @property
    def is_readable(self):
        """Is this public or am I the owner?"""
        if self.is_public or self.is_owner:
            return True
        else:
            return False

    @property
    def is_public(self):
        """Is this accessible to anyone?"""
        return self.public

    def is_owner(self, user):
        """Is the user the owner of the of the Template?"""
        if user == self.user:
            return True
        return False

    def get_url(self, request=None):
        """ Return a URL for this object - Not the direct S3 Object"""
        return get_template_url(self, request)

    def get_reverse(self, action, request):
        """ Return the full URL of the action request (e.g. template-list) """
        return reverse_lazy(action, request=request)

    def __str__(self):
        return f'{self.uuid}'

    class Meta:
        verbose_name = 'Templates'
        verbose_name_plural = 'Templates'
