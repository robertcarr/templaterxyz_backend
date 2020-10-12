from django.db import models
from django.conf import settings

from utils.core import get_shortuuid, get_upload_folder

# Create your models here.

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


class Templates(models.Model):
    """
    Describes a Template in the system.

    The template can be public or private.
    Templates can be anonymous or owned by a registered user.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=22, default=get_shortuuid, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repos, on_delete=models.CASCADE, related_name='repo')

    template = models.FileField(upload_to=get_upload_folder, blank=False)
    params = models.FileField(upload_to=get_upload_folder, blank=False)

    public = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Templates'
        verbose_name_plural = 'Templates'
