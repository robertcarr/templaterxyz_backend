"""
Custom Content Negotiation for special use case

Use Text Renderer for GET and JSON for everything else
"""
from rest_framework.negotiation import BaseContentNegotiation, DefaultContentNegotiation

from utils.render import PlainTextRenderer


class CustomContentNegotiation(DefaultContentNegotiation):
    """
    If a request is GET return PlainTextRenderer instead of JSON
    """
    def select_renderer(self, request, renderers, format_suffix=None):
        return (PlainTextRenderer, 'text/plain')

