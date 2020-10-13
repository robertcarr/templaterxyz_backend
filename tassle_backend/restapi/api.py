# API Endpoint mapping to Viewsets

from utils.routers import OptionalSlashRouter
from .viewsets import TemplateViewset

router = OptionalSlashRouter()
router.register(r'', TemplateViewset, basename='template')
