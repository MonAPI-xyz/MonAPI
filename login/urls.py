from django.urls import path
from login import views

urlpatterns = [
    path('', views.user_login, name='login'),
    
    # New authentication path
    path('login/', views.user_login, name='auth-login'),
    path('logout/', views.user_logout, name='auth-logout'),
    path('current_team/', views.current_team, name='auth-current-team'),
    path('available_team/', views.available_team, name='auth-available-team'),
    path('change_team/', views.change_team, name='auth-change-team'),
    path('list_member/', views.list_member, name='auth-list-member')
]