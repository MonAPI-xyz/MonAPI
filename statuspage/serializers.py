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
        
        read_only_fields = ['team']

class APIMonitorSuccessRateSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    success = serializers.IntegerField()
    failed = serializers.IntegerField()

class StatusPageDashboardSerializers(serializers.ModelSerializer):
    success_rate_category = APIMonitorSuccessRateSerializer(many=True)
    class Meta:
        model = StatusPageCategory
        fields = [
            'id',
            'name',
            'success_rate_category',
        ]