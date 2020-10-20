# API Endpoint mapping to Viewsets

from django.urls import path, include

from utils.routers import OptionalSlashRouter
from .viewsets import TemplateViewset, StatsViewset

router = OptionalSlashRouter()
router.register(r'stats/', StatsViewset, basename='stats')
router.register(r'^$', TemplateViewset, basename='template')
