from rest_framework.routers import DefaultRouter


class OptionalSlashRouter(DefaultRouter):
    """
    Make trailing slash optional
    """
    def __init__(self, *args, **kwargs):
        super(OptionalSlashRouter, self).__init__()
        self.trailing_slash = '\/?'

