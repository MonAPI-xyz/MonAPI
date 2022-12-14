from django.urls import path, include
from rest_framework import routers
from statuspage.views import StatusPageConfigurationView, StatusPageCategoryViewSet, StatusPageDashboardViewSet

router = routers.DefaultRouter()
router.register(r'', StatusPageCategoryViewSet, basename='statuspage-category')

urlpatterns = [
    path('category/', include(router.urls)),
    path('config/', StatusPageConfigurationView.as_view(), name='statuspage-config'),
    path('dashboard/', StatusPageDashboardViewSet.as_view({'get': 'list'}), name='statuspage-dashboard'),
]