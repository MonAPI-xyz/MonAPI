from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import views, status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apimonitor.models import APIMonitorResult
from statuspage.models import StatusPageConfiguration, StatusPageCategory
from statuspage.serializers import StatusPageConfgurationSerializers, StatusPageCategorySerializers, StatusPageDashboardSerializers

class StatusPageConfigurationView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):        
        config, _ = StatusPageConfiguration.objects.get_or_create(team=request.auth.team)
        serializer = StatusPageConfgurationSerializers(config)
        return Response(serializer.data)
    
    def post(self, request, format=None):        
        config, _ = StatusPageConfiguration.objects.get_or_create(team=request.auth.team)
        serializer = StatusPageConfgurationSerializers(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class StatusPageCategoryViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    
    queryset = StatusPageCategory.objects.all()
    serializer_class = StatusPageCategorySerializers
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        queryset = StatusPageCategory.objects.filter(team=self.request.auth.team)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = StatusPageCategorySerializers(data=request.data)
        if serializer.is_valid():
            status_page = StatusPageCategory.objects.create(
                team = request.auth.team,
                name = serializer.data['name'],
            )
            serializer = StatusPageCategorySerializers(status_page)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StatusPageDashboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = StatusPageCategory.objects.all()
    serializer_class = StatusPageDashboardSerializers
    permission_classes = []
    pagination_class = None

    def list(self, request):
        status_page_config = StatusPageConfiguration.objects.filter(path=self.request.GET.get('path'))
        if len(status_page_config) == 0:
            return Response(data={"error": "Please make sure your URL path is exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = StatusPageCategory.objects.filter(team=status_page_config[0].team)

        for category in queryset:
            success_rate_category = []
            api_monitor_result_count = APIMonitorResult.objects \
                .filter(monitor__status_page_category=category).count()

            if api_monitor_result_count == 0:
                category.success_rate_category = success_rate_category
                continue
            
            #success_rate per category
            last_24_hour = timezone.now() - timedelta(hours=24)
            for _ in range(24):
                start_time = last_24_hour
                end_time = last_24_hour + timedelta(hours=1)
                
                # Average success rate
                success_count = APIMonitorResult.objects.filter(
                    monitor__status_page_category=category, 
                    execution_time__gte=start_time, 
                    execution_time__lte=end_time
                ).aggregate(
                    s=Count('success', filter=Q(success=True)), 
                    f=Count('success', filter=Q(success=False)),
                    total=Count('pk'),
                )

                success_rate_category.append({
                    "start_time": start_time,
                    "end_time" : end_time,
                    "success": success_count['s'],
                    "failed" : success_count['f']
                })

                last_24_hour += timedelta(hours=1)

            category.success_rate_category = success_rate_category

        serializer = StatusPageDashboardSerializers(queryset, many=True)
        return Response(serializer.data)