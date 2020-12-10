import json

from rest_framework import serializers

from .models import Templates, Stats



class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ('templates_rendered', 'templates_saved', )


class TemplatesSerializer(serializers.ModelSerializer):
    IDX = 0
    id = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()

    def get_params(self, obj):
        try:
            return json.loads(obj.params.read())
        except:
            return None

    def get_template(self, obj):
        try:
            return obj.template.read()
        except:
            return None

    def get_id(self, obj):
        self.IDX += 1
        return self.IDX

    class Meta:
        model = Templates
        fields = (
            'id',
            'created',
            'modified',
            'uuid',
            'public',
            'name',
            'description',
            'template',
            'params'
        )
