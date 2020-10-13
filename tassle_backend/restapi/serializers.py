from rest_framework import serializers

from .models import Templates

class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = (
            'created',
            'modified',
            'uuid',
            'public',
            'name',
            'description'
        )
