from rest_framework import serializers

from statuspage.models import StatusPageConfiguration, StatusPageCategory

class StatusPageConfgurationSerializers(serializers.ModelSerializer):
    class Meta:
        model = StatusPageConfiguration
        fields = [
            'path',
        ]
        

class StatusPageCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StatusPageCategory
        fields = [
            'id',
            'team',
            'name',
        ]