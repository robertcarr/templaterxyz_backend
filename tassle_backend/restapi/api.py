# API Endpoint mapping to Viewsets

from django.urls import path, include

from utils.routers import OptionalSlashRouter
from .viewsets import TemplateViewset, StatsViewset, TemplateDetailViewset

router = OptionalSlashRouter()
# lookup a specific template.  regex in viewset
router.register(r'', TemplateDetailViewset, basename='tz')
router.register(r'stats/', StatsViewset, basename='stats')
router.register(r'^$', TemplateViewset, basename='template')
