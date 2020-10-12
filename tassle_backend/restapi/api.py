# API Endpoint mapping to Viewsets
from rest_framework.routers import DefaultRouter

from .viewsets import TemplateViewset

router = DefaultRouter()
router.register(r'', TemplateViewset, basename='template')