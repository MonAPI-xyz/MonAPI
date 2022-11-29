from django.shortcuts import render
from rest_framework import views, status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from statuspage.models import StatusPageConfiguration, StatusPageCategory
from statuspage.serializers import StatusPageConfgurationSerializers, StatusPageCategorySerializers

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
        request.data['team'] = request.auth.team.pk
        return super().create(request, *args, **kwargs)
    